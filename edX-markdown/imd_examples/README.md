## How to write imd files

* [Here](http://edx.readthedocs.io/projects/edx-guide-for-students/en/latest/completing_assignments/SFD_mathformatting.html)
 is the reference to the mathematical expression allowed on edX.

#### Python code
1. Wrap the python code with the following with no space at front.

	\`\`\`python

	\`\`\`

2. Use python code to define random variables. It is recommended to have random variables in the problem so that different students see slightly different problems.

3. Define solutions for all the questions in the problem. ```solution1``` is the solution for the first part. ```solution2``` is the solution for the second part.

4. You can't assign a variable to solutions. Solution variables have to be assigned with a string directly. For example, you **can't** do

        a = "3*5"
        solution1 = a

      instead, you need to do

        solution1 = "3*5"

      or
        a = "3*5"
        solution1 = "{}".format(a)

5. When there is power operation "\*\*", change it to "^". Also wrap the exponent with {}. For example, ```2^n``` will need to be written as

        "2^{{{0}}}".format(n)
      or
        "2^{%d}"%n

  If you don't have any variable in the exponent, you can simply write

        2^{10}

#### imd code
	1. Please format the problem nicely using markdown syntax. Bullet points are highly recommended.

	2. Math expression can be inline or on a new line. If you want to have inline math expression use "$" to wrap the expression. If you want the math expression on a new line, use "$$".

	3. Variables from the python code can be refer by adding ```\$``` at front. For example, if variable ```n``` is used in the markdown code, use ```\$n``` instead.

	4. Place ```[_]``` where you want an input box to appear. Make sure your input box is in a newline. In Markdown, you need to have a newline above and a newline below ```[_]```. We don't want to have inline input box, so always have a new line before the input box and a new line after.

	5. After you finish the problem, double check to make sure the solutions you defined in your python code match the order of the questions in the problem.

#### Different types of problems
* Check box

  [ ] and [x] stands for the check box. [x] represent the box that need to be checked.

  Example:

      [ ] This is a wrong choice
      [x] This is a right choice
      [ ] This is another wrong choice
      [x] This is another right choice

* Drop down list

	[\_choice] stands for a drop down list. If [\_choice] is found as the first input box, ```option1``` and ```solution1``` are expected in the python code.

	Example:

      ```Python
      option1 = ('True', 'False', 'Null')
      solution1 = "True"
      solution2 = "3*5"
      solution3 = "2-1+6"
      option4 = ('A', 'B', 'C')
      solution4 = "B"
      ```
      First question. Please select one answer from the drop down list.

      [_choice]

      Second question. Please fill in the box below.

      [_]

      Third question. Please fill in the box below.

      [_]

      Fourth question. Please select one answer from the drop down list.

      [_choice]
