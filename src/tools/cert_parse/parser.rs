/*
 * parser.rs
 *
 * Copyright (C) 2025 Alessandro Iepure
 * SPDX-License-Identifier: GPL-3.0-or-later
*/

use std::net::{Ipv4Addr, Ipv6Addr};

use gettextrs::{gettext, pgettext};
use md5::{Digest, Md5};
use sha1::Sha1;
use x509_parser::{
    asn1_rs::Oid,
    certificate::X509Certificate,
    extensions::{DistributionPointName, GeneralName, ParsedExtension},
    objects::{oid2sn, oid_registry},
    parse_x509_certificate,
    pem::Pem,
    public_key::PublicKey,
    signature_algorithm::SignatureAlgorithm,
};

use std::fmt::Write;

// Extension category for UI grouping
enum ExtCategory {
    Named,
    General,
    Other,
}

/// Value of a certificate field for display purposes.
#[derive(Debug, Clone)]
pub enum CertFieldValue {
    /// Plain text
    Text(String),
    /// Raw bytes displayed as hexadecimal
    HexData(Vec<u8>),
    /// List of strings
    List(Vec<String>),
}

/// A single field in a certificate section
#[derive(Debug, Clone)]
pub struct CertField {
    pub label: String,
    pub value: CertFieldValue,
}

/// Named section grouping related certificate fields
#[derive(Debug, Clone)]
pub struct CertSection {
    pub title: String,
    pub fields: Vec<CertField>,
}

/// Complete result from parsing a certificate
#[derive(Debug, Clone)]
pub struct CertParseResult {
    pub identity: String,
    pub verifier: String,
    pub not_before: String,
    pub not_after: String,
    pub serial: String,
    pub version: String,
    pub public_key_sections: Vec<CertSection>,
    pub signature_algorithm_section: CertSection,
    pub signature_value_section: CertSection,
    pub fingerprint_sha1: Vec<u8>,
    pub fingerprint_md5: Vec<u8>,
    pub named_extensions: Vec<CertSection>,
    pub general_extensions: Vec<CertSection>,
    pub other_extensions: Vec<CertSection>,
}

/// Parse an x.509 certificate from DER or PEM encoded bytes
pub fn parse_certificate(data: &[u8]) -> Result<CertParseResult, String> {
    // Try DER first
    if let Ok((_, cert)) = parse_x509_certificate(data) {
        return build_result(data, &cert);
    }

    // Try PEM
    for pem_result in Pem::iter_from_buffer(data) {
        let pem = pem_result.map_err(|e| {
            pgettext("Error", "Failed to parse PEM: {e}").replace("{e}", &e.to_string())
        })?;
        if let Ok((_, cert)) = parse_x509_certificate(&pem.contents) {
            return build_result(&pem.contents, &cert);
        }
    }

    Err(gettext("Could not parse certificate as DER or PEM"))
}

/// Result construction helper function
fn build_result(data: &[u8], cert: &X509Certificate<'_>) -> Result<CertParseResult, String> {
    let identity = cert.subject().to_string();
    let verifier = cert.issuer().to_string();
    let not_before = cert.validity().not_before.to_string();
    let not_after = cert.validity().not_after.to_string();
    let serial = cert.tbs_certificate.raw_serial_as_string().to_string();
    let version = format_version(cert.version());

    let public_key_sections = build_public_key_sections(cert);
    let signature_algorithm_section = build_signature_algorithm_section(cert);
    let signature_value_section = build_signature_value_section(cert);

    let fingerprint_sha1 = compute_fingerprint::<Sha1>(data);
    let fingerprint_md5 = compute_fingerprint::<Md5>(data);

    let (named_extensions, general_extensions, other_extensions) = build_extension_sections(cert);

    Ok(CertParseResult {
        identity,
        verifier,
        not_before,
        not_after,
        serial,
        version,
        public_key_sections,
        signature_algorithm_section,
        signature_value_section,
        fingerprint_sha1,
        fingerprint_md5,
        named_extensions,
        general_extensions,
        other_extensions,
    })
}

// ------------------------------------------
// MARK: Formatting helpers
// ------------------------------------------
fn format_version(version: x509_parser::x509::X509Version) -> String {
    let v = version.0;
    if v == 0 || v == 1 || v == 2 {
        format!("V{version}")
    } else {
        format!("INVALID({v})")
    }
}

fn format_oid(oid: &Oid) -> String {
    match oid2sn(oid, oid_registry()) {
        Ok(s) => s.to_owned(),
        Err(_) => oid.to_string(),
    }
}

fn compute_fingerprint<D: Digest>(data: &[u8]) -> Vec<u8> {
    D::digest(data).to_vec()
}

fn format_general_name(gn: &GeneralName) -> String {
    match gn {
        GeneralName::DNSName(name) => format!("DNS:{name}"),
        GeneralName::DirectoryName(n) => format!("DirName:{n}"),
        GeneralName::EDIPartyName(obj) => format!("EDIPartyName:{obj:?}"),
        GeneralName::IPAddress(b) => {
            let ip = match b.len() {
                4 => {
                    let arr: Option<[u8; 4]> = (*b).try_into().ok();
                    arr.map(|a| Ipv4Addr::from(a).to_string())
                        .unwrap_or_else(|| format!("invalid IPv4: {b:?}"))
                }
                16 => {
                    let arr: Option<[u8; 16]> = (*b).try_into().ok();
                    arr.map(|a| Ipv6Addr::from(a).to_string())
                        .unwrap_or_else(|| format!("invalid IPv6: {b:?}"))
                }
                l => format!("invalid IP (len={l})"),
            };
            format!("IP Address:{ip}")
        }
        GeneralName::OtherName(oid, val) => format!("OtherName: {oid} {val:?}"),
        GeneralName::RFC822Name(name) => format!("RFC822:{name}"),
        GeneralName::RegisteredID(oid) => format!("RegisteredID:{oid}"),
        GeneralName::URI(uri) => format!("URI:{uri}"),
        GeneralName::X400Address(obj) => format!("X400Address:{obj:?}"),
        GeneralName::Invalid(tag, data) => {
            format!("Invalid: tag={}, data={:?}", tag.0, data)
        }
    }
}

// Used in widget
pub fn format_hex_data(bytes: &[u8], num: usize, label: &str) -> String {
    let indent = " ".repeat(label.len() + 6);
    let mut output = String::new();
    for (i, chunk) in bytes.chunks(num).enumerate() {
        if i > 0 {
            output.push('\n');
            output.push_str(&indent);
        }
        for byte in chunk {
            write!(&mut output, "{byte:02X} ").unwrap();
        }
    }
    output.trim_end().to_string()
}

// ------------------------------------------
// MARK: Builders
// ------------------------------------------
fn build_public_key_sections(cert: &X509Certificate<'_>) -> Vec<CertSection> {
    let pubkey = cert.public_key();
    let mut sections = Vec::new();

    // Algorithm section
    let mut alg_fields = vec![CertField {
        label: gettext("Algorithm"),
        value: CertFieldValue::Text(format_oid(&pubkey.algorithm.algorithm)),
    }];
    if let Some(params) = &pubkey.algorithm.parameters {
        if let Ok(oid) = params.as_oid() {
            alg_fields.push(CertField {
                label: gettext("Parameters"),
                value: CertFieldValue::Text(format_oid(&oid)),
            })
        } else {
            let tag = format!("{:?}", params.tag());
            alg_fields.push(CertField {
                label: gettext("Parameters"),
                value: CertFieldValue::Text(format!("tag={tag}")),
            });
            // if let Ok(bytes) = params.as_bytes() {
            //     alg_fields.push(CertField {
            //         label: gettext("Parameters"),
            //         value: CertFieldValue::HexData(bytes.to_vec()),
            //     })
            // }
            alg_fields.push(CertField {
                label: gettext("Parameters"),
                value: CertFieldValue::HexData(params.as_bytes().to_vec()),
            })
        }
    }
    sections.push(CertSection {
        title: gettext("Public Key Algorithm"),
        fields: alg_fields,
    });

    // Parse key data
    match pubkey.parsed() {
        Ok(PublicKey::RSA(rsa)) => {
            sections.push(CertSection {
                title: gettext("RSA public key ({n_bits} bit)")
                    .replace("{n_bits}", &rsa.key_size().to_string()),
                fields: vec![
                    CertField {
                        label: gettext("Modulus"),
                        value: CertFieldValue::HexData(rsa.modulus.to_vec()),
                    },
                    CertField {
                        label: gettext("Exponent"),
                        value: if let Ok(e) = rsa.try_exponent() {
                            CertFieldValue::Text(format!("0x{e:x} ({e})"))
                        } else {
                            CertFieldValue::HexData(rsa.exponent.to_vec())
                        },
                    },
                ],
            });
        }
        Ok(PublicKey::EC(ec)) => sections.push(CertSection {
            title: gettext("EC public key ({n_bits} bit)")
                .replace("{n_bits}", &ec.key_size().to_string()),
            fields: vec![CertField {
                label: gettext("Public Key"),
                value: CertFieldValue::HexData(ec.data().to_vec()),
            }],
        }),
        Ok(PublicKey::DSA(dsa)) => sections.push(CertSection {
            title: gettext("DSA public key ({n_bits} bit)")
                .replace("{n_bits}", &(8 * dsa.len()).to_string()),
            fields: vec![CertField {
                label: gettext("Public Key"),
                value: CertFieldValue::HexData(dsa.to_vec()),
            }],
        }),
        Ok(PublicKey::GostR3410(y)) => {
            sections.push(CertSection {
                title: gettext("GOST R 34.10-94 Public Key ({n_bits} bit)")
                    .replace("{n_bits}", &(8 * y.len()).to_string()),
                fields: vec![CertField {
                    label: gettext("Public Key"),
                    value: CertFieldValue::HexData(y.to_vec()),
                }],
            });
        }
        Ok(PublicKey::GostR3410_2012(y)) => {
            sections.push(CertSection {
                title: gettext("GOST R 34.10-2012 Public Key ({n_bits} bit)")
                    .replace("{n_bits}", &(8 * y.len()).to_string()),
                fields: vec![CertField {
                    label: gettext("Public Key"),
                    value: CertFieldValue::HexData(y.to_vec()),
                }],
            });
        }
        Ok(PublicKey::Unknown(b)) => {
            sections.push(CertSection {
                title: gettext("Unknown Public Key"),
                fields: vec![CertField {
                    label: gettext("Raw Data"),
                    value: CertFieldValue::HexData(b.to_vec()),
                }],
            });
        }
        Err(_) => {
            sections.push(CertSection {
                title: gettext("Public Key"),
                fields: vec![CertField {
                    label: gettext("Status"),
                    value: CertFieldValue::Text(gettext("Could not parse public key")),
                }],
            });
        }
    }

    sections
}

fn build_signature_algorithm_section(cert: &X509Certificate<'_>) -> CertSection {
    let sig_alg = &cert.signature_algorithm;
    let mut fields = Vec::new();

    match SignatureAlgorithm::try_from(sig_alg) {
        Ok(alg) => {
            let name = match &alg {
                SignatureAlgorithm::DSA => "DSA",
                SignatureAlgorithm::ECDSA => "ECDSA",
                SignatureAlgorithm::ED25519 => "ED25519",
                SignatureAlgorithm::RSA => "RSA",
                SignatureAlgorithm::RSASSA_PSS(_) => "RSASSA-PSS",
                SignatureAlgorithm::RSAAES_OAEP(_) => "RSAAES-OAEP",
            };
            fields.push(CertField {
                label: gettext("Algorithm"),
                value: CertFieldValue::Text(name.to_string()),
            });

            if let SignatureAlgorithm::RSASSA_PSS(params) = &alg {
                fields.push(CertField {
                    label: gettext("Hash Algorithm"),
                    value: CertFieldValue::Text(format_oid(params.hash_algorithm_oid())),
                });
                if let Ok(mask_gen) = params.mask_gen_algorithm() {
                    fields.push(CertField {
                        label: gettext("Mask Generation Function"),
                        value: CertFieldValue::Text(format!(
                            "{}/{}",
                            format_oid(&mask_gen.mgf),
                            format_oid(&mask_gen.hash)
                        )),
                    });
                }
                fields.push(CertField {
                    label: gettext("Salt Length"),
                    value: CertFieldValue::Text(params.salt_length().to_string()),
                });
            } else if let SignatureAlgorithm::RSAAES_OAEP(params) = &alg {
                fields.push(CertField {
                    label: gettext("Hash Algorithm"),
                    value: CertFieldValue::Text(format_oid(params.hash_algorithm_oid())),
                });
                if let Ok(mask_gen) = params.mask_gen_algorithm() {
                    fields.push(CertField {
                        label: gettext("Mask Generation Function"),
                        value: CertFieldValue::Text(format!(
                            "{}/{}",
                            format_oid(&mask_gen.mgf),
                            format_oid(&mask_gen.hash)
                        )),
                    });
                }
                fields.push(CertField {
                    label: gettext("PSourceFunc"),
                    value: CertFieldValue::Text(format_oid(&params.p_source_alg().algorithm)),
                });
            }
        }
        Err(_) => {
            fields.push(CertField {
                label: gettext("Algorithm OID"),
                value: CertFieldValue::Text(format_oid(&sig_alg.algorithm)),
            });
            if let Some(params) = &sig_alg.parameters {
                if !params.as_bytes().is_empty() {
                    fields.push(CertField {
                        label: gettext("Parameters"),
                        value: CertFieldValue::HexData(params.as_bytes().to_vec()),
                    })
                }
            }
        }
    }

    CertSection {
        title: gettext("Signature Algorithm"),
        fields,
    }
}

fn build_signature_value_section(cert: &X509Certificate<'_>) -> CertSection {
    CertSection {
        title: gettext("Signature Value"),
        fields: vec![CertField {
            label: gettext("Value"),
            value: CertFieldValue::HexData(cert.signature_value.as_ref().to_vec()),
        }],
    }
}

fn build_extension_sections(
    cert: &X509Certificate<'_>,
) -> (Vec<CertSection>, Vec<CertSection>, Vec<CertSection>) {
    let mut named = Vec::new();
    let mut general = Vec::new();
    let mut other = Vec::new();

    for ext in cert.extensions() {
        let section = match ext.parsed_extension() {
            // Named extensions
            ParsedExtension::BasicConstraints(bc) => {
                let val = if bc.ca {
                    gettext("True")
                } else {
                    gettext("False")
                };
                Some((
                    ExtCategory::Named,
                    CertSection {
                        title: gettext("Basic Constraints"),
                        fields: vec![CertField {
                            label: "CA".to_string(),
                            value: CertFieldValue::Text(val.to_string()),
                        }],
                    },
                ))
            }
            ParsedExtension::KeyUsage(ku) => Some((
                ExtCategory::Named,
                CertSection {
                    title: gettext("Key Usage"),
                    fields: vec![CertField {
                        label: gettext("Usage"),
                        value: CertFieldValue::Text(ku.to_string()),
                    }],
                },
            )),
            ParsedExtension::ExtendedKeyUsage(eku) => {
                let mut oids = Vec::new();
                if eku.server_auth {
                    oids.push("serverAuth".to_string());
                }
                if eku.client_auth {
                    oids.push("clientAuth".to_string());
                }
                if eku.code_signing {
                    oids.push("codeSigning".to_string());
                }
                if eku.email_protection {
                    oids.push("emailProtection".to_string());
                }
                if eku.time_stamping {
                    oids.push("timeStamping".to_string());
                }
                if eku.ocsp_signing {
                    oids.push("OCSPSigning".to_string());
                }
                if eku.any {
                    oids.push("anyExtendedKeyUsage".to_string());
                }
                for oid in &eku.other {
                    oids.push(format_oid(oid));
                }
                Some((
                    ExtCategory::Named,
                    CertSection {
                        title: gettext("Extended Key Usage"),
                        fields: vec![CertField {
                            label: gettext("Usages"),
                            value: CertFieldValue::List(oids),
                        }],
                    },
                ))
            }
            ParsedExtension::SubjectKeyIdentifier(ski) => Some((
                ExtCategory::Named,
                CertSection {
                    title: "Subject Key Identifier".to_string(),
                    fields: vec![CertField {
                        label: gettext("Key Identifier"),
                        value: CertFieldValue::HexData(ski.0.to_vec()),
                    }],
                },
            )),
            ParsedExtension::SubjectAlternativeName(san) => {
                let names: Vec<String> =
                    san.general_names.iter().map(format_general_name).collect();
                Some((
                    ExtCategory::Named,
                    CertSection {
                        title: gettext("Subject Alternative Names"),
                        fields: vec![CertField {
                            label: gettext("Names"),
                            value: CertFieldValue::List(names),
                        }],
                    },
                ))
            }

            // General extensions
            ParsedExtension::AuthorityKeyIdentifier(aki) => {
                let mut fields = Vec::new();
                if let Some(key_id) = &aki.key_identifier {
                    fields.push(CertField {
                        label: gettext("Key Identifier"),
                        value: CertFieldValue::HexData(key_id.0.to_vec()),
                    });
                }
                if let Some(issuer) = &aki.authority_cert_issuer {
                    let names: Vec<String> = issuer.iter().map(format_general_name).collect();
                    fields.push(CertField {
                        label: gettext("Certificate Issuer"),
                        value: CertFieldValue::List(names),
                    });
                }
                if let Some(serial) = &aki.authority_cert_serial {
                    fields.push(CertField {
                        label: gettext("Certificate Serial"),
                        value: CertFieldValue::HexData(serial.to_vec()),
                    });
                }
                Some((
                    ExtCategory::General,
                    CertSection {
                        title: gettext("Authority Key Identifier"),
                        fields,
                    },
                ))
            }
            ParsedExtension::CRLDistributionPoints(points) => {
                let mut fields = Vec::new();
                for (i, point) in points.iter().enumerate() {
                    let label = if points.len() > 1 {
                        gettext("Distribution Point {num}").replace("{num}", &(i + 1).to_string())
                    } else {
                        gettext("Distribution Point")
                    };

                    let mut desc = String::new();
                    if let Some(name) = &point.distribution_point {
                        let names: Vec<String> = match name {
                            DistributionPointName::FullName(names) => {
                                names.iter().map(format_general_name).collect()
                            }
                            DistributionPointName::NameRelativeToCRLIssuer(rdn) => {
                                vec![format!("NameRelativeToCRLIssuer({rdn:?})")]
                            }
                        };
                        desc.push_str(
                            &gettext("Full Name: {name}").replace("{name}", &names.join(", ")),
                        );
                    }

                    if let Some(reasons) = &point.reasons {
                        if !desc.is_empty() {
                            desc.push_str("; ");
                        }
                        desc.push_str(
                            &gettext("Reasons: {reasons}")
                                .replace("{reasons}", &reasons.to_string()),
                        );
                    }

                    if let Some(crl_issuer) = &point.crl_issuer {
                        if !desc.is_empty() {
                            desc.push_str("; ");
                        }
                        let names: Vec<String> =
                            crl_issuer.iter().map(format_general_name).collect();
                        write!(&mut desc, "CRL Issuer: {}", names.join(", ")).unwrap();
                    }

                    fields.push(CertField {
                        label,
                        value: CertFieldValue::Text(desc),
                    });
                }

                Some((
                    ExtCategory::General,
                    CertSection {
                        title: gettext("CRL Distribution Points"),
                        fields,
                    },
                ))
            }
            ParsedExtension::IssuerAlternativeName(ian) => {
                let names: Vec<String> =
                    ian.general_names.iter().map(format_general_name).collect();
                Some((
                    ExtCategory::General,
                    CertSection {
                        title: gettext("Issuer Alternative Name"),
                        fields: vec![CertField {
                            label: gettext("Names"),
                            value: CertFieldValue::List(names),
                        }],
                    },
                ))
            }
            ParsedExtension::CertificatePolicies(policies) => {
                let oids: Vec<String> = policies
                    .iter()
                    .map(|pi| format_oid(&pi.policy_id))
                    .collect();
                Some((
                    ExtCategory::General,
                    CertSection {
                        title: gettext("Certificate Policies"),
                        fields: vec![CertField {
                            label: gettext("Policies"),
                            value: CertFieldValue::List(oids),
                        }],
                    },
                ))
            }

            // Other extensions
            _ => {
                let oid_str = format_oid(&ext.oid);
                Some((
                    ExtCategory::Other,
                    CertSection {
                        title: gettext("Extension"),
                        fields: vec![
                            CertField {
                                label: "OID".to_string(),
                                value: CertFieldValue::Text(oid_str),
                            },
                            CertField {
                                label: "Value".to_string(),
                                value: CertFieldValue::HexData(ext.value.to_vec()),
                            },
                        ],
                    },
                ))
            }
        };

        if let Some((category, section)) = section {
            match category {
                ExtCategory::Named => named.push(section),
                ExtCategory::General => general.push(section),
                ExtCategory::Other => other.push(section),
            }
        }
    }

    (named, general, other)
}
