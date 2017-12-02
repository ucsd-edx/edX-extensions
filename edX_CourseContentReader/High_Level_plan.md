## A plan for edX content modularization

### Long term goals
Our long term goal is to create a content authoring layer above edX that would allow content creators: instructors, TAs, tutors, to manipulate course content in any desired level. Archive and search through problems and connect units into paths.

### Short term plan
On the short term, the goals are to modify the code Zhen wrote to do the following. My hope is that this is overall a pretty small change.
* Translate an exported tar ball into a  courseware data structure in memory, and translate a courseware data structure back to a tar ball that can be imported into edX.
* Fix the problem of multiple hashes.
* generate markdown files for origin and incoming.
* Combine two trees using the three markdown method: origin , incoming and new.
* Translate the new tree into a tar ball.

The main technical change is that the courseware data structure should be generic and contain all of the information in the tar ball. This can be done by using an XML parser (I  used [xml.etree.elementtree](https://docs.python.org/2/library/xml.etree.elementtree.html#module-xml.etree.ElementTree) this way guarantees that the data-structure contains all of the information in the tar ball, and the information is organized in a consistent way.

### Longer term plan

1. Allow simplified manipulation of parameters such as "number of tries" and "problem weight" for problems and "open date" "due date" for assignments.

2. Break down a tar ball into the elements that define it, giving each unit a meaningful file name, rather than a random hash. These files can then put into a github repository.

3. Once units have meaningful names, constructing a course can be done by writing a markdown file with references to the different units. The code will then generate the tar-ball for edX.

4. Having modular units will allow arranging the units into a graph describing which units are pre-requisites to others.

5. Adaptive hints and adaptive paths for students will be possible to the degree that edX allows them.  Zhen identified the following documentation for "jumps" between edX units:
  * http://help.appsembler.com/article/171-how-to-link-to-a-specific-unit-within-your-course
  * http://files.edx.org/handouts/stopgap/Add_a_Link_to_a_Course_Unit.pdf
It basically use the “jump_to_id”.


