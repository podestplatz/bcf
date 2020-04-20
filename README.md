# BCF Python

It is a free software library for the reading and writing of the [BCF (BIM
Collaboration Format)](https://en.wikipedia.org/wiki/BIM_Collaboration_Format)
in Python. It implements [BCF-XML](https://github.com/buildingSMART/BCF-XML).

# Dependencies

Following you will find a list of non standard python modules that might have to be installed 
manually:

- [python-dateutil](https://pypi.org/project/python-dateutil/)
- [xmlschema](https://pypi.org/project/xmlschema/)
- [pytz](https://pypi.org/project/pytz/)
- [pyperclip](https://pypi.org/project/pyperclip)

I reccommend installing these packages inside a [python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). To 
create one in the current directory, and subsequently activate it, execute:

```bash
$> python3 -m venv <NAME>
$> source ./<NAME>/bin/activate
```

# Usage

To get access to the nonGUI-frontend (also called programmatic interface or PI for short) the import of `bcfplugin` suffices. 
```python
>>> import bcfplugin as plugin
```
This imports all necessary functions into the plugin global namespace from `programmaticInterface.py`, thereby making them easily accessible.

Without a BCF file, however, the plugin is of little value, thus let's open a BCF file: 
```python
>>> plugin.openProject("/path/to/bcf/file.bcf")
```
**Note**: If you use a file that does not comply with the standard, then you will see some error messages in the `Report view`. These notify you about the fact that a particular file could not be validated successfully against the corresponding XSD-(XML Schema Definition)File. For every non valid file one error message is printed. A more detailed version of the errors, specifying which node exactly did not comply, can be found in the log file. The path of the log file will be printed before any of these error messages are displayed. 

But that doesn't have to concern you right now. Every node that does not comply with the standard is simply not read into the internal data model. That means you can't modify it, but still can add/update/delete to/from the model. 

To read all available topics, ordered by index run:

```python
>>> plugin.getTopics()
```

This function returns you a list of tuples. Each tuple does contain the title of the topic as first element, the second element is a reference to the topic object itself. These references are important, so save them in a variable like: 

```python 
>>> topics = [ topic[1] for topic in plugin.getTopics() ]
```

You might also want to view all comments in chronological order, related with one topic, say the first one in the list: 

```python
>>> plugin.getComments(topics[0])
```

As it was the case with the topics, `getComments()` also returns a list of tuples, here the first element is the comment itself with the name of the creator, the date of creation and the date of last modification.

But comments alone would be pretty boring, so you can retrieve a list of viewpoints associated with a given topic with

```python
>>> plugin.getViewpoints(topics[0])
```

Again, you receive a list of tuples. Apart from the reference to the viewpoint object, you get the file name of the viewpoint as first element of the tuple. 
There might be cases where you just want to view comments that are linked to certain viewpoints in a topic. To generate a list like this run:

```python
>>> viewpoints = [ vp[1] for vp in plugin.getViewpoints(topic[0]) ]
>>> plugin.getComments(topic[0], viewpoints[0])
```

In a topic might also be some IFC project files listed that the topic is associated with. You can review a list of these with: 
```python
>>> plugin.getRelevantIfcFiles(topics[0])
```

And to get a list of related documents the function `getAdditionalDocumentReferences()` is the one for you: 

```python
>>> plugin.getAdditionalDocumentReferences(topics[0])
```

You might have noticed by now that the topic is a rather important object, so treat it with care!
If you stumble upon a member `id` in any object you retrieved from the plugin, don't modify it. The plugin uses this member to uniquely identify objects in the data model!
