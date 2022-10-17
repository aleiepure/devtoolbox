# Devtoolbox documentation - TextArea widget

[Home](../readme.md) / TextArea
### Contents
 - [Description](#description)
 - [GtkBuildable](#gtkbuildable)
 - [Properties](#properties)
 - [Signals](#signals)
 - [Methods](#methods)
---
## Description
A widget where text can be directly inserted with options to open a file (see below), copy all the text, paste from the clipboard, clear the entry and execute a custom action. All buttons are individually showable using the relatives property.
Loaded files are automatically checked for their content and as plain text. An error is thrown if it is not text.
All text is syntax highlighted if the property `text-syntax-highlight` is set and the correct language is selected in `text_language_highlight`.

[↩️ to top](#)

---

## GtkBuildable
```xml
<object class="TextArea" id="_text_area">
    <property name="name">Input</property>
    <property name="show-open-btn">true</property>
    <property name="show-paste-btn">true</property>
    <property name="show-clear-btn">true</property>
    <property name="use-default-text-extensions">true</property>
</object>
```
[↩️ to top](#)

---
## Properties
  - [name](#name)
  - [show-clear-btn](#show-clear-btn)
  - [show-copy-btn](#show-copy-btn)
  - [show-open-btn](#show-open-btn)
  - [show-paste-btn](#show-paste-btn)
  - [show-action-btn](#show-action-btn)
  - [action-name](#action-name)
  - [text-editable](#text-editable)
  - [text-show-line-numbers](#text-show-line-numbers)
  - [text-highlight-current-line](#text-highlight-current-line)
  - [text-syntax-highlighting](#text-syntax-highlighting)
  - [text-language-highlight](#text-language-highlight)
  - [area-height](#area-height)
  - [use-default-text-extensions](#use-default-text-extensions)
  - [use-custom-file-extensions](#use-custom-file-extensions)
  - [custom-file-extensions](#custom-file-extensions)

[↩️ to top](#)

### **name**
```
property name: string
```
Label used as the title of the section. Default is `""`.\
[↩️ to properties](#properties)

### **show-clear-btn**
```
property show-clear-btn: bool
```
Shows or hides the clear button. Default is `False`.\
[↩️ to properties](#properties)

### **show-copy-btn**
```
property show-copy-btn: bool
```
Shows or hides the copy button. Default is `False`.\
[↩️ to properties](#properties)

### **show-open-btn**
```
property show-open-btn: bool
```
Shows or hides the open button. Default is `False`.\
[↩️ to properties](#properties)

### **show-paste-btn**
```
property show-paste-btn: bool
```
Shows or hides the paste button. Default is `False`.\
[↩️ to properties](#properties)

### **show-action-btn**
```
property show-action-btn: bool
```
Shows or hides the action button. Set this property to be able to invoke a custom function on the input. Default is `False`.\
[↩️ to properties](#properties)

### **action-name**
```
property action-name: string
```
Label used for the action button. Dependes on `show-action-btn` set as `TRUE`.  Default is `""`.\
[↩️ to properties](#properties)

### **text-editable**
```
property text-editable: bool
```
Makes the textbox responsive to keyboard inputs.  Default is `True`.\
[↩️ to properties](#properties)

### **text-show-line-numbers**
```
property text-show-line-numbers: bool
```
Shows or hides the left gutter with line numbers.  Default is `False`.\
[↩️ to properties](#properties)

### **text-highlight-current-line**
```
property text-highlight-current-line: bool
```
Highlights the line where the cursor is located.  Default is `False`.\
[↩️ to properties](#properties)

### **text-syntax-highlighting**
```
property text-syntax-highlighting: bool
```
Highlights the text with the syntax specified in `text-language-syntax`. Default is `False`.\
[↩️ to properties](#properties)

### **text-language-highlight**
```
property text-language-highlight: string
```
Specifies the language used to highlight keywords in the text. The expected result works only if `text-syntax-highlighting` is set to `True`. Default is `""`.\
[↩️ to properties](#properties)

### **area-height**
```
property area-height: int
```
Specifies the height in pixels of the input area when is empty. If the text overflows the available space, the input area grown to contain it all. Default is `200`.\
[↩️ to properties](#properties)

### **use-default-text-extensions**
```
property use-default-text-extensions: bool
```
Specifies if the file dialog should show or not text files as an available format to open. Default is `False`.\
[↩️ to properties](#properties)

### **custom-file-extensions**
```
property custom-file-extensions: string[]
```
List of file extension (without leading `.`) that the file dialog shows to open. As a GtkBuildable, the array items are specified as a newline-separated list:
```xml
<property name="custom-file-extensions">mp3
    mp4
    mkv
</property>
```
[↩️ to properties](#properties)

---
## Signals
  - [action-clicked](#action-clicked)
  - [text-changed](#text-changed)
  - [view-cleared](#view-cleared)
  - [text-loaded](#text-loaded)
  - [big-file](#big-file)
  - [error](#error)
  
[↩️ to top](#)


### **action-clicked**
```
signal action-clicked(source_widget, user_data)
```
Emited when the user clicks the action button.\
[↩️ to signals](#signals)

### **text-changed**
```
signal text-changed(source_widget, user_data)
```
Emited when the user causes a visible change of the text (i.e. types, pastes, deletes, etc.).\
[↩️ to signals](#signals)

### **view-cleared**
```
signal view-cleared(source_widget, user_data)
```
Emited when the user clicks the clear button.\
[↩️ to signals](#signals)

### **text-loaded**
```
signal text-loaded(source_widget, user_data)
```
Emited when the file chosen with the open file dialog is recognized as text and is finished loading.\
[↩️ to signals](#signals)

### **big-file**
```
signal big-file(source-widget, user_data)
```
Emited when the file chosen with the open file dialog is larger than 1GB.\
[↩️ to signals](#signals)

### **error**
```
signal error(source_widget, error, user_data)
```
Emited when an error occurs inside the widget. The error description is contained in `error` as a `string`.\
[↩️ to signals](#signals)

---
## Methods
  - [get_text](#get_text)
  - [get_buffer](#get_buffer)
  - [set_text_language_highlight](#set_text_language_highlight)
  - [add_css_class](#add_css_class)
  - [remove_css_class](#remove_css_class)
  - [enable_copy_btn](#enable_copy_btn)
  
[↩️ to top](#)


### **get_text**
```
string get_text()
```
Returns the text currently present in the widget.\
[↩️ to methods](#methods)

### **get_buffer**
```
GtkTextBuffer get_buffer()
```
Returns the `GtkTextBuffer` associated with the widget.\
[↩️ to methods](#methods)

### **set_visible_view**
```
void set_visible_view(string view_name)
```
Sets the type of view currently visible in the widget. Note that the only possible values for the parameter are `text` and `image`.\
[↩️ to methods](#methods)

### **set_text_language_highlight**
```
void set_text_language_highlight(string language)
```
Sets the language used for syntax highlighting in the widget.\
[↩️ to methods](#methods)

### **add_css_class**
```
void add_css_class(string class)
```
Wrapper around `GtkWidget::add_css_class()` to apply css classes to the widget.\
[↩️ to methods](#methods)

### **remove_css_class**
```
void remove_css_class(string class)
```
Wrapper around `GtkWidget::remove_css_class()` to remove css classes from the widget.\
[↩️ to methods](#methods)

### **enable_copy_btn**
```
void enable _copy_btn(bool enabled)
```
Sets whether or not the copy button (if shown with `show-copy-btn`) is clickable.\
[↩️ to methods](#methods)