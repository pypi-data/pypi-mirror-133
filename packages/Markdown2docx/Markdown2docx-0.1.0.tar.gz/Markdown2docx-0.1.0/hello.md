![hello](hello.png "A hello title")

<!--- 
MaCrOs

  // You can make comments // or # and skip blank lines

{'__customer__':'Example Customer Name really long'}
{'__div__':'Division'}
# You can run commands
{'__date__':'${date}'}
// You can combine variable substitution and commands
{'__customer_date__':'__customer__ __div__ ${date}'}

// and substitution for command arguments:
{'__example__':'${./some_command __div__}'}


END_MaCrOs
---> 

Today's date: __date__

# Hello world markdown to docx
## Table of contents for __customer__
To insert a table of contents, use the word 'contents' embedded somewhere. The first (and only) time Markdown2docx.py finds this trigger, it will insert a table of contents field. The user will be prompted to update the field when opening the .docx output document.

#### Token substitution
This tool will allow you to create .docx output from standard markdown text but with a twist: You can declare tokens or commands in one or more sections within comment blocks delimited by MaCrOs:

![macros](macros.png "A Macro")


Where key is surrounded by two underscore characters. Using this idea, words or phrases used repeatedly may be declared as macros.

<!--- 
MaCrOs

  // Later definitions override earlier definitions

{'__customer__':'My Customer'}

END_MaCrOs
---> 

Furthermore, anywhere that a command exists using the format 💲{mycommand}, the output of that command will be inserted into the final .docx document. Token substitution is done first which means you can also use 💲{mycommand ＿myarg1＿}. It's ok to put multiple commands into the same line. It's ok to have multiple tokens in the same line and in the same command if required.





### Horizontal rules
There are two ways to make a horizontal rule:

```
---
- - -
```
---
- - -

### Bold and emphasis.
This conversion tool was written to gather data from machine configuration and often, these include variable names with underscores like_this_example. In a markdown reader, you'll note that the word 'this' is rendered as italics while the underscore spacing has been consumed. To get around it, one must use a backslash \\ to escape the underscore like\\\_this\\\_example which is rendered like\_this\_example.

This is likely to cause a lot of re-work to manually fix it, especially if there are hundereds of such variable names in the source. While it's possible to write a filter to change the source and insert the escape characters, that's extra work. Markdown2docx could also try to recognise when the escape characters are needed, but then we have an issue if the underscore is already escaped. How do we know that it's already escaped, or it should be left as-is if that was the intention? Therefore, Markdown2docx passes the underscore without transformation. 

For words that are bolded like **this** (\*\*this\*\*) or emphasised like *this* (\*this\*) it's a similar story. 

How much is lost due to this decision? I'd argue almost nothing. It's not only rare in literature to use italics, in some situations it's undesirable. Bold text might be useful in technical writing, but it doesn't add to the meaning of the text unless it's a declared typographical convension. If you really must have the odd italic or bold word or paragraph, please consider changing it manually once the .docx document is made.

### Bullets
These are bullets--i.e. an "unordered list". We can do only three levels deep before using a workaround and the bullets symbol will be ○.

* point 1
* point 2
* level 1
	* sub point 2
	* sub point 3 
	* level 2
		* sub sub point 4
		* level 3
			* level 5
			* level 5
				* level 6
					* level 7	 
* point 4

### Numbered lists
Like bullets, there is a restriction of three levels. Levels deeper than that will use a default symbol. (#)

1. first line
2. second line
	1. Two point 1
	2. Two point 2
		1. Two point two point 1
			1. Two point two point one point one
			2. Two point two point one point two
		2. Two point two point 2
	3. Two point 3
	4. Two point 4
3. third line    
	 
	


## Header 2 Chap 1

Chapter 1 example.

## Header 2 Chap 2

Chapter 2 example.

## Header 2 Chap 3

Chapter 3 example.

### Header 3 - quoted text

A smaller header:

```
Quoted text
   indented
   _underscored_
```

## Header 2 Chap 4

An even smaller header:

#### Header 4
A tiny heading

## Tables

Text here.

#### A times table
|1|2|3|4|5|
|---|---|---|---|---|
|1|2|3|4|5|
|2|4|6|8|10|
|3|6|9|12|15
|4|8|12|16|20|
|5|10|15|20|25

More text here.

#### Another table
|aa|bb|cc|
|----|----|----|
|11|22|33|
|33|44|55|

# Lena
Pictures smaller than 70% of the width of the target document are not scaled down. They will appear actual size. The assumed "ok" DPI is 200 pixels per inch.

![lenna](lenna.png "A lena title")

# How to use Markdown2docx.py

Here is how to use the module without tokens or command substitution.

```
#!/usr/bin/env python3
import Markdown2docx as m2

project = m2.Markdown2docx('hello')
project.eat_soup()
project.save()
```
You can print the styles used like this:

```
#!/usr/bin/env python3
import Markdown2docx as m2

project = m2.Markdown2docx('hello')
project.eat_soup()
project.write_html()  # optional
print(type(project.styles()))  # Optional
for k, v in project.styles().items():  # Optional
    print(f'stylename: {k} = {v}')  # Optional
project.save()
```


In this example, "hello" is the base name of the input "hello.md". This is your markdown source. It's best to use a markdown editor to get it right before rendering in .docx format.

The output is hello.docx and may be opened in Microsoft Word.

eat_soup() is the method that converts the input markdown to .docx. At this point, it's only held in memory. Use the save() method to write it to disk.

## Optional Markdown2docx functions

* To get a web-browser compatible HTML output, use the write_html() method.

```
write_html()
```

* To print the current styles use the following code:

```
for k, v in project.styles().items():
    print(f'stylename: {k} = {v}')
```

# Coding with tokens and command substitution

```
#!/usr/bin/env python3

from PreprocessMarkdown2docx import PreprocessMarkdown2docx
import Markdown2docx as m2

project = 'hello'
ppm2w = PreprocessMarkdown2docx(project)
macros = ppm2w.macros
markdown = ppm2w.get_all_but_macros()
markdown = ppm2w.do_substitute_tokens(markdown)
markdown = ppm2w.do_execute_commands(markdown)
project = m2.Markdown2docx(project, markdown)
project.eat_soup()
project.write_html()  # optional
project.save()
```
