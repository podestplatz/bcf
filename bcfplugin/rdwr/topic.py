"""
Copyright (C) 2019 PODEST Patrick

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

"""
Author: Patrick Podest
Date: 2019-08-16
Github: @podestplatz

**** Description ****
This file provides classes that are necessary to represent the contents of a
Topic node inside a markup.bcf file.
"""

import xml.etree.ElementTree as ET
from copy import deepcopy
from typing import List
from enum import Enum
from uuid import UUID
from datetime import date
from xmlschema import XMLSchema

import bcfplugin.util
from bcfplugin.rdwr.modification import (ModificationDate, ModificationAuthor,
        ModificationType)
from bcfplugin.rdwr.uri import Uri
from bcfplugin.rdwr.project import (Attribute, SimpleElement, SimpleList,
        searchListObject, listSetContainingElement)
from bcfplugin.rdwr.interfaces.hierarchy import Hierarchy
from bcfplugin.rdwr.interfaces.identifiable import XMLIdentifiable, Identifiable
from bcfplugin.rdwr.interfaces.state import State
from bcfplugin.rdwr.interfaces.xmlname import XMLName


class DocumentReference(Hierarchy, State, XMLName, Identifiable):

    """ Represents the XML type markup.xsd:DocumentReference """

    def __init__(self,
                guid: UUID = None,
                external: bool = False,
                reference: Uri = None,
                description: str = "",
                containingElement = None,
                state: State.States = State.States.ORIGINAL):

        """ Initialization function for DocumentReference """

        Hierarchy.__init__(self, containingElement)
        State.__init__(self, state)
        XMLName.__init__(self)
        Identifiable.__init__(self)
        self._guid = Attribute(guid, "Guid", UUID(int=0), self)
        self._external = Attribute(external, "isExternal", False, self)
        self._reference = SimpleElement(reference, "ReferencedDocument",
                None, self)
        self._description = SimpleElement(description, "Description",
                "", self)


    def __deepcopy__(self, memo):

        """ Create a deepcopy of the object without copying `containingObject`
        """

        cpyid = deepcopy(self.id, memo)
        cpyguid = deepcopy(self._guid, memo)
        cpyexternal = deepcopy(self._external, memo)
        cpyreference = deepcopy(self._reference, memo)
        cpydescription = deepcopy(self._description, memo)

        cpy = DocumentReference()
        cpy._guid = cpyguid
        cpy._external = cpyexternal
        cpy._reference = cpyreference
        cpy._description = cpydescription
        cpy.id = cpyid
        cpy.state = self.state

        members = [ cpy._guid, cpy._external, cpy._reference, cpy._description ]
        listSetContainingElement(members, cpy)

        return cpy


    def __eq__(self, other):

        """
        Returns true if every variable member of both classes are the same
        """

        if type(self) != type(other):
            return False

        return (self.guid == other.guid and
                self.external == other.external and
                self.reference == other.reference and
                self.description == other.description)


    def __str__(self):
        str_ret = ("DocumentReference(guid={}, external={}, reference={},"\
            " description={})").format(self.guid, self.external, self.reference,
                self.description)

        return str_ret


    @property
    def guid(self):
        return self._guid.value

    @guid.setter
    def guid(self, newVal):
        if isinstance(newVal, str):
            self._guid.value = UUID(newVal)
        elif isinstance(newVal, UUID):
            self._guid.value = newVal

    @property
    def external(self):
        return self._external.value

    @external.setter
    def external(self, newVal):
        self._external.value = newVal

    @property
    def reference(self):
        return self._reference.value

    @reference.setter
    def reference(self, newVal):
        self._reference.value = newVal

    @property
    def description(self):
        return self._description.value

    @description.setter
    def description(self, newVal):
        self._description.value = newVal

    def getEtElement(self, elem):

        """
        Convert the contents of the object to an xml.etree.ElementTree.Element
        representation. `element` is the object of type xml.e...Tree.Element
        which shall be modified and returned.
        """

        elem.tag = self.xmlName

        # guid is optional in DocumentReference
        defaultValue = self._guid.defaultValue
        if self.guid != defaultValue:
            elem.attrib["Guid"] = str(self.guid)

        defaultValue = self._external.defaultValue
        if self.external != defaultValue:
            elem.attrib["isExternal"] = str(self.external).lower()

        defaultValue = self._reference.defaultValue
        if str(self.reference) != defaultValue:
            refElem = ET.SubElement(elem, "ReferencedDocument")
            refElem.text = str(self.reference)

        defaultValue = self._description.defaultValue
        if self.description != defaultValue:
            descElem = ET.SubElement(elem, "Description")
            descElem.text = self.description

        return elem


    def getStateList(self):

        stateList = list()
        if not self.isOriginal():
            stateList.append((self.state, self))

        stateList += self._guid.getStateList()
        stateList += self._external.getStateList()
        stateList += self._reference.getStateList()
        stateList += self._description.getStateList()

        return stateList


    def searchObject(self, object):

        if not issubclass(type(object), Identifiable):
            return None

        id = object.id
        if self.id == id:
            return self

        members = [ self._guid, self._external, self._reference,
                self._description ]
        searchResult = searchListObject(object, members)
        return searchResult


class RelatedTopic(Hierarchy, State, XMLName, Identifiable):

    """ Represents the XML type markup.xsd:RelatedTopic """

    def __init__(self,
            guid: UUID = None,
            containingElement = None,
            state: State.States = State.States.ORIGINAL):

        Hierarchy.__init__(self, containingElement)
        State.__init__(self, state)
        XMLName.__init__(self)
        Identifiable.__init__(self)
        self._guid = Attribute(guid, "Guid", UUID(int=0), self)

    def __deepcopy__(self, memo):

        """ Create a deepcopy of the object without copying `containingObject`
        """

        cpyid = deepcopy(self.id, memo)
        cpyguid = deepcopy(self._guid, memo)

        cpy = RelatedTopic()
        cpy._guid = cpyguid
        cpy.id = cpyid
        cpy.state = self.state

        members = [ cpy._guid ]
        listSetContainingElement(members, cpy)

        return cpy


    def __eq__(self, other):

        """
        Returns true if every variable member of both classes are the same
        """

        if type(self) != type(other):
            return False

        return self.guid == other.guid

    def __str__(self):

        ret_str = ("RelatedTopic(guid='{}')").format(self.guid)
        return ret_str


    @property
    def guid(self):
        return self._guid.value

    @guid.setter
    def guid(self, newVal):
        if isinstance(newVal, str):
            self._guid.value = UUID(newVal)
        elif isinstance(newVal, UUID):
            self._guid.value = newVal

    def getEtElement(self, elem):

        """
        Convert the contents of the object to an xml.etree.ElementTree.Element
        representation. `element` is the object of type xml.e...Tree.Element
        which shall be modified and returned.
        """

        print('in the get et element of relatedtopic')
        #elem.tag = "RelatedTopic"
        elem.tag = self.xmlName
        elem.attrib["Guid"] = str(self.guid)

        return elem


    def getStateList(self):

        stateList = list()
        if not self.isOriginal():
            stateList.append((self.state, self))

        stateList += self._guid.getStateList()

        return stateList


    def searchObject(self, object):

        if not issubclass(type(object), Identifiable):
            return None

        id = object.id
        if self.id == id:
            return self

        members = [ self._guid ]
        searchResult = searchListObject(object, members)
        return searchResult



class BimSnippet(Hierarchy, State, XMLName, Identifiable):

    """ Represents the XML type markup.xsd:BimSnippet """

    def __init__(self,
            type: str = "",
            external: bool = False,
            reference: Uri = None,
            schema: Uri = None,
            containingElement = None,
            state: State.States = State.States.ORIGINAL):

        """ Initialization function for BimSnippet """

        Hierarchy.__init__(self, containingElement)
        State.__init__(self, state)
        XMLName.__init__(self)
        Identifiable.__init__(self)
        self._type = Attribute(type, "SnippetType", "", self)
        self._external = Attribute(external, "isExternal", False, self)
        self._reference = SimpleElement(reference, "Reference", None, self)
        self._schema = SimpleElement(schema, "ReferenceSchema", None, self)


    def __deepcopy__(self, memo):

        """ Create a deepcopy of the object without copying `containingObject`
        """

        cpyid = deepcopy(self.id, memo)
        cpytype = deepcopy(self._type, memo)
        cpyexternal = deepcopy(self._external, memo)
        cpyreference = deepcopy(self._reference, memo)
        cpyschema = deepcopy(self._schema, memo)

        cpy = BimSnippet()
        cpy._type = cpytype
        cpy._external = cpyexternal
        cpy._reference = cpyreference
        cpy._schema = cpyschema
        cpy.id = cpyid
        cpy.state = self.state

        members = [ cpy._type, cpy._external, cpy._reference, cpy._schema ]
        listSetContainingElement(members, cpy)

        return cpy


    def __eq__(self, other):

        """
        Returns true if every variable member of both classes are the same
        """

        if type(self) != type(other):
            return False

        return (self.type == other.type and
                self.external == other.external and
                self.reference == other.reference and
                self.schema == other.schema)

    def __str__(self):

        ret_str = ("BimSnippet(type='{}', isExternal='{}, reference='{}',"\
                " referenceSchema='{}'").format(self.type, self.external,
                        self.reference, self.schema)
        return ret_str


    @property
    def type(self):
        return self._type.value

    @type.setter
    def type(self, newVal):
        self._type.value = newVal

    @property
    def external(self):
        return self._external.value

    @external.setter
    def external(self, newVal):
        self._external.value = newVal

    @property
    def reference(self):
        return self._reference.value

    @reference.setter
    def reference(self, newVal):
        self._reference.value = newVal

    @property
    def schema(self):
        return self._schema.value

    @schema.setter
    def schema(self, newVal):
        self._schema.value = newVal

    def getEtElement(self, elem):

        """
        Convert the contents of the object to an xml.etree.ElementTree.Element
        representation. `element` is the object of type xml.e...Tree.Element
        which shall be modified and returned.
        """

        elem.tag = "BimSnippet"
        elem.attrib["SnippetType"] = str(self.type)
        elem.attrib["isExternal"] = str(self.external).lower()

        defaultValue = self._reference.defaultValue
        if self.reference != defaultValue:
            refElem = ET.SubElement(elem, "Reference")
            refElem.text = str(self.reference)

        defaultValue = self._schema.defaultValue
        if self.schema != defaultValue:
            schemaElem = ET.SubElement(elem, "ReferenceSchema")
            schemaElem.text = str(self.schema)

        return elem


    def getStateList(self):

        stateList = list()
        if not self.isOriginal():
            stateList.append((self.state, self))

        stateList += self._type.getStateList()
        stateList += self._external.getStateList()
        stateList += self._reference.getStateList()
        stateList += self._schema.getStateList()

        return stateList


    def searchObject(self, object):

        if not issubclass(type(object), Identifiable):
            return None

        id = object.id
        if self.id == id:
            return self

        members = [ self._type, self._external, self._reference, self._schema ]
        searchResult = searchListObject(object, members)

        return searchResult


class Topic(Hierarchy, XMLIdentifiable, State, XMLName, Identifiable):

    """ Represents the XML type markup.xsd:Topic """

    def __init__(self,
            id: UUID,
            title: str,
            date: ModificationDate,
            author: ModificationAuthor,
            type: str = "",
            status: str = "",
            referenceLinks: List[str] = list(),
            docRefs: List[DocumentReference] = list(),
            priority: str = "",
            index: int = -1,
            labels: List[str] = list(),
            modDate: ModificationDate = None,
            modAuthor: ModificationAuthor = "",
            dueDate: date = None,
            assignee: str = "",
            description: str = "",
            stage: str = "",
            relatedTopics: List[RelatedTopic] = [],
            bimSnippet: BimSnippet = None,
            containingElement = None,
            state: State.States = State.States.ORIGINAL):

        """ Initialisation function of Topic """

        Hierarchy.__init__(self, containingElement)
        XMLIdentifiable.__init__(self, id)
        State.__init__(self, state)
        XMLName.__init__(self)
        Identifiable.__init__(self)
        self._title = SimpleElement(title, "Title", "", self)
        self._date = ModificationDate(date, self)
        self._author = ModificationAuthor(author, self)
        self._type = Attribute(type, "TopicType", "", self)
        self._status = Attribute(status, "TopicStatus", "", self)
        self.referenceLinks = SimpleList(referenceLinks, "ReferenceLink",
                "", self)
        self.docRefs = docRefs
        self._priority = SimpleElement(priority, "Priority", "", self)
        self._index = SimpleElement(index, "Index", -1, self)
        self.labels = SimpleList(labels, "Labels", "", self)
        self._modDate = ModificationDate(modDate, self,
                ModificationType.MODIFICATION)
        self._modAuthor = ModificationAuthor(modAuthor, self,
                ModificationType.MODIFICATION)
        self._dueDate = SimpleElement(dueDate, "DueDate", None, self)
        self._assignee = SimpleElement(assignee, "AssignedTo", "", self)
        self._description = SimpleElement(description, "Description",
                "", self)
        self._stage = SimpleElement(stage, "Stage", "", self)
        self.relatedTopics = relatedTopics
        self.bimSnippet = bimSnippet

        # set containingObjecf for all document references
        for docRef in self.docRefs:
            docRef.containingObject = self

        if self.bimSnippet is not None:
            self.bimSnippet.containingObject = self


    def __deepcopy__(self, memo):

        """ Create a deepcopy of the object without copying `containingObject`
        """

        cpyid = deepcopy(self.id, memo)
        cpyxmlid = deepcopy(self.xmlId, memo)
        cpytitle = deepcopy(self._title, memo)
        cpydate = deepcopy(self._date, memo)
        cpyauthor = deepcopy(self._author, memo)
        cpytype = deepcopy(self._type, memo)
        cpystatus = deepcopy(self._status, memo)
        cpyreferencelinks = deepcopy(self.referenceLinks, memo)
        cpydocrefs = deepcopy(self.docRefs, memo)
        cpypriority = deepcopy(self._priority, memo)
        cpyindex = deepcopy(self._index, memo)
        cpylabels = deepcopy(self.labels, memo)
        cpymoddate = deepcopy(self._modDate, memo)
        cpymodauthor = deepcopy(self._modAuthor, memo)
        cpyduedate = deepcopy(self._dueDate, memo)
        cpyassignee = deepcopy(self._assignee, memo)
        cpydescription = deepcopy(self._description, memo)
        cpystage = deepcopy(self._stage, memo)
        cpyrelatedtopics = deepcopy(self.relatedTopics, memo)
        cpybimsnippet = deepcopy(self.bimSnippet, memo)

        cpy = Topic(cpyxmlid, None, None, None)
        cpy._title = cpytitle
        cpy._date = cpydate
        cpy._author = cpyauthor
        cpy._type = cpytype
        cpy._status = cpystatus
        cpy.referenceLinks = cpyreferencelinks
        cpy.docRefs = cpydocrefs
        cpy._priority = cpypriority
        cpy._index = cpyindex
        cpy.labels = cpylabels
        cpy._modDate = cpymoddate
        cpy._modAuthor = cpymodauthor
        cpy._dueDate = cpyduedate
        cpy._assignee = cpyassignee
        cpy._description = cpydescription
        cpy._stage = cpystage
        cpy.relatedTopics = cpyrelatedtopics
        cpy.bimSnippet = cpybimsnippet
        cpy.id = cpyid
        cpy.state = self.state

        listSetContainingElement(cpy.referenceLinks, cpy)
        listSetContainingElement(cpy.labels, cpy)
        listSetContainingElement(cpy.relatedTopics, cpy)
        members = [ cpy._title, cpy._date, cpy._author, cpy._type, cpy._status,
                cpy._priority, cpy._index, cpy._modDate, cpy._modAuthor,
                cpy._dueDate, cpy._assignee, cpy._description, cpy._stage,
                cpy.bimSnippet ]
        listSetContainingElement(members, cpy)

        return cpy


    def __eq__(self, other):

        """
        Returns true if every variable member of both classes are the same
        """

        if type(self) != type(other):
            return False

        return (self.xmlId == other.xmlId and
                self.title == other.title and
                self.__checkNone(self.date, other.date) and
                self.author == other.author and
                self.type == other.type and
                self.status == other.status and
                self.docRefs == other.docRefs and
                self.priority == other.priority and
                self.index == other.index and
                self.labels == other.labels and
                self.__checkNone(self.modDate, other.modDate) and
                self.modAuthor, other.modAuthor and
                self.__checkNone(self.dueDate, other.dueDate) and
                self.assignee == other.assignee and
                self.description == other.description and
                self.stage == other.stage and
                self.relatedTopics == other.relatedTopics and
                self.bimSnippet == other.bimSnippet)

    def __str__(self):

        doc_ref_str = "None"
        if self.docRefs:
            doc_ref_str = "["
            for doc_ref in self.docRefs:
                doc_ref_str += str(doc_ref)
            doc_ref_str += "]"

        str_ret = """---- Topic ----
    ID: {},
    Title: {},
    Date: {},
    Author: {},
    Type: {},
    Status: {},
    Priority: {},
    Index: {},
    ModificationDate: {},
    ModificationAuthor: {},
    DueDate: {},
    AssignedTo: {},
    Description: {},
    Stage: {},
    RelatedTopics: {},
    Labels: {},
    DocumentReferences: {}""".format(self.xmlId, self.title, str(self.date),
            self.author,
            self.type, self.status, self.priority, self.index,
            str(self.modDate), self.modAuthor, self.dueDate,
            self.assignee, self.description, self.stage, self.relatedTopics,
            self.labels, doc_ref_str)
        return str_ret


    @property
    def date(self):
        return self._date.value

    @date.setter
    def date(self, newVal):
        self._date.date = newVal

    @property
    def author(self):
        return self._author.value

    @author.setter
    def author(self, newVal):
        self._author.author = newVal

    @property
    def modDate(self):
        return self._modDate.value

    @modDate.setter
    def modDate(self, newVal):
        self._modDate.date = newVal

    @property
    def modAuthor(self):
        return self._modAuthor.value

    @modAuthor.setter
    def modAuthor(self, newVal):
        self._modAuthor.author = newVal

    @property
    def stage(self):
        return self._stage.value

    @stage.setter
    def stage(self, newVal):
        self._stage.value = newVal

    @property
    def description(self):
        return self._description.value

    @description.setter
    def description(self, newVal):
        self._description.value = newVal

    @property
    def assignee(self):
        return self._assignee.value

    @assignee.setter
    def assignee(self, newVal):
        self._assignee.value = newVal

    @property
    def dueDate(self):
        return self._dueDate.value

    @dueDate.setter
    def dueDate(self, newVal):
        self._dueDate.value = newVal

    @property
    def index(self):
        return self._index.value

    @index.setter
    def index(self, newVal):
        self._index.value = newVal

    @property
    def priority(self):
        return self._priority.value

    @priority.setter
    def priority(self, newVal):
        self._priority.value = newVal

    @property
    def status(self):
        return self._status.value

    @status.setter
    def status(self, newVal):
        self._status.value = newVal

    @property
    def type(self):
        return self._type.value

    @type.setter
    def type(self, newVal):
        self._type.value = newVal

    @property
    def title(self):
        return self._title.value

    @title.setter
    def title(self, newVal):
        self._title.value = newVal


    def __checkNone(self, this, that):

        """ Checks whether `this` and `that` are equal considering "None"
        values """

        equal = False
        if this and that:
            equal = this == that
        elif (this is None and that is None):
            equal = True
        return equal


    def __eq__(self, other):

        """
        Returns true if every variable member of both classes are the same
        """

        if type(self) != type(other):
            return False

        return (self.xmlId == other.xmlId and
                self.title == other.title and
                self.__checkNone(self.date, other.date) and
                self.author == other.author and
                self.type == other.type and
                self.status == other.status and
                self.docRefs == other.docRefs and
                self.priority == other.priority and
                self.index == other.index and
                self.labels == other.labels and
                self.__checkNone(self.modDate, other.modDate) and
                self.modAuthor, other.modAuthor and
                self.__checkNone(self.dueDate, other.dueDate) and
                self.assignee == other.assignee and
                self.description == other.description and
                self.stage == other.stage and
                self.relatedTopics == other.relatedTopics and
                self.bimSnippet == other.bimSnippet)

    def __str__(self):

        doc_ref_str = "None"
        if self.docRefs:
            doc_ref_str = "["
            for doc_ref in self.docRefs:
                doc_ref_str += str(doc_ref)
            doc_ref_str += "]"

        str_ret = """---- Topic ----
    ID: {},
    Title: {},
    Date: {},
    Author: {},
    Type: {},
    {}: {},
    Priority: {},
    Index: {},
    {}: {},
    {}: {},
    DueDate: {},
    AssignedTo: {},
    Description: {},
    Stage: {},
    RelatedTopics: {},
    Labels: {},
    DocumentReferences: {}""".format(self.xmlId, self.title, str(self.date),
            self.author,
            self.type, self._status.xmlName, self.status, self.priority, self.index,
            self._modDate.xmlName, str(self.modDate), self._modAuthor.xmlName,
            self.modAuthor, self.dueDate, self.assignee, self.description,
            self.stage, self.relatedTopics, self.labels, doc_ref_str)
        return str_ret


    def _createSimpleNode(self, parentNode: ET.Element,
            classMember: SimpleElement):

        """ Create an ET.Element containing the serialized content of
        `classMember`.

        The new element will be a sub-element of `parentNode`.
        """

        newNode = None
        dflValue = classMember.defaultValue
        if classMember.value != dflValue:
            newNode = ET.SubElement(parentNode, classMember.xmlName)
            newNode = classMember.getEtElement(newNode)

        return newNode


    def getEtElement(self, elem):

        """
        Convert the contents of the object to an xml.etree.ElementTree.Element
        representation. `element` is the object of type xml.e...Tree.Element
        which shall be modified and returned.
        """

        elem.tag = self.xmlName
        elem.attrib["Guid"] = str(self.xmlId)

        defaultValue = self._type.defaultValue
        if self.type != defaultValue:
            elem.attrib[self._type.xmlName] = self.type

        defaultValue = self._status.defaultValue
        if self.status != defaultValue:
            elem.attrib[self._status.xmlName] = self.status

        for refLink in self.referenceLinks:
            refLinkElem = self._createSimpleNode(elem, refLink)

        titleElem = ET.SubElement(elem, "Title")
        titleElem = self._title.getEtElement(titleElem)

        prioElem = self._createSimpleNode(elem, self._priority)
        idxElem = self._createSimpleNode(elem, self._index)

        for lbl in self.labels:
            lblElem = self._createSimpleNode(elem, lbl)

        dateElem = ET.SubElement(elem, "Date")
        dateElem = self._date.getEtElement(dateElem)

        authorElem = ET.SubElement(elem, "Author")
        authorElem = self._author.getEtElement(authorElem)

        if self.modDate is not None:
            modDateElem = self._createSimpleNode(elem,
                    self._modDate)
            modAuthorElem = self._createSimpleNode(elem,
                    self._modAuthor)

        dueDateElem = self._createSimpleNode(elem, self._dueDate)
        assigneeElem = self._createSimpleNode(elem, self._assignee)
        stageElem = self._createSimpleNode(elem, self._stage)
        descElem = self._createSimpleNode(elem, self._description)

        if self.bimSnippet is not None:
            bimSnippetElem = ET.SubElement(elem, self.bimSnippet.xmlName)
            bimSnippetElem = self.bimSnippet.getEtElement(bimSnippetElem)

        for docRef in self.docRefs:
            docRefElem = ET.SubElement(elem, docRef.xmlName)
            docRefElem = docRef.getEtElement(docRefElem)

        for relTopic in self.relatedTopics:
            relatedTopicElem = ET.SubElement(elem, relTopic.xmlName)
            relatedTopicElem = relTopic.getEtElement(relatedTopicElem)

        return elem


    def getStateList(self):

        stateList = list()
        if not self.isOriginal():
            stateList.append((self.state, self))

        stateList += self._title.getStateList()
        stateList += self.creation.getStateList()
        stateList += self._type.getStateList()
        stateList += self._status.getStateList()
        stateList += self.referenceLinks.getStateList()
        for ref in self.refs:
            stateList += ref.getStateList()

        stateList += self._priority.getStateList()
        stateList += self._index.getStateList()
        stateList += self.labels.getStateList()
        if self.lastModification is not None:
            stateList += self.lastModification.getStateList()

        stateList += self._dueDate.getStateList()
        stateList += self._assignee.getStateList()
        stateList += self._description.getStateList()
        stateList += self._stage.getStateList()
        stateList += self.relatedTopics.getStateList()
        if self.bimSnippet is not None:
            stateList += self.bimSnippet.getStateList()

        return stateList


    def searchObject(self, object):

        if not issubclass(type(object), Identifiable):
            return None

        id = object.id
        if self.id == id:
            return self

        members = [ self._title, self._date, self._author, self._type,
                self._status, self._priority, self._index, self._modDate,
                self._modAuthor, self._dueDate, self._assignee,
                self._description, self._stage, self.bimSnippet ]
        searchResult = searchListObject(object, members)
        if searchResult is not None:
            return searchResult

        searchResult = searchListObject(object, self.referenceLinks)
        if searchResult is not None:
            return searchResult

        searchResult = searchListObject(object, self.docRefs)
        if searchResult is not None:
            return searchResult

        searchResult = searchListObject(object, self.labels)
        if searchResult is not None:
            return searchResult

        searchResult = searchListObject(object, self.relatedTopics)
        if searchResult is not None:
            return searchResult

        return None
