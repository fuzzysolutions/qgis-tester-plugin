.. (c) 2016 Boundless, http://boundlessgeo.com
   This code is licensed under the GPL 2.0 license.

Writing tests
=============

Tester plugin does not contain any test, they are distributed either as part of other plugins (to test this specific plugin) or as separate plugins containing only tests (for example, for QGIS core functionality) and nothing else.

To write a new set of tests, add a new python module file in the to the plugin, it can be inside plugin's root directory or in the separate folder, e.g. inside *tests* folder. The module can have two functions, to define unit tests (automated) and functional tests (semi-automated):  ``unitTests()`` and ``functionalTests()`` respectively. None of these functions is mandatory. The Tester plugin will look for them and, if found, will call them to retrieve the tests declared by the module.

Plugins should register their tests suite to the Tester plugin by using the ``addTestModule()`` function. To do this add following code in your plugin's ``__init__()`` method (don't forget to replace ``from plugin.tests import testmodule`` with correct import of the module with tests)

::

    try:
        from plugin.tests import testmodule
        from qgistester.tests import addTestModule
        addTestModule(testmodule, "Tests_category_or_name")
    except:
        pass

Also to correctly de-register plugin's tests from the Tester plugin add following code to the plugin's ``unload()`` method

::

    try:
        from plugin.tests import testmodule
        from qgistester.tests import removeTestModule
        removeTestModule(testmodule, 'Tests_category_or_name')
    except:
        pass


Unit Tests
**********

Unit tests are created by wrapping a Python test suite. Create your test suite in the usual Python way and then return it from the ``unitTests()`` method.

The test description shown in the test selector dialog is taken from the test's ``shortDescription()`` method, which takes the first line of the docstring, so if you want to add a name to your test, just add a one-line dosctring to it. If no docstring is present, the test method name will be used.

Functional Tests
****************

Functional tests are defined using the *Test* class from the ``qgistester.test`` module. Here is an example of a functional test suite containing single test which in turn consists of two steps (one automated and one manual)

::

    def functionalTests():
	    vectorRenderingTest = Test("Verify rendering of uploaded style")
	    vectorRenderingTest.addStep("Preparing data", _openAndUpload)
	    vectorRenderingTest.addStep("Check that WMS layer is correctly rendered")
	    vectorRenderingTest.setCleanup(_clean)

        return [vectorRenderingTest]

First we need to create a new instance of the ``Test`` class. Constructor accepts two parameters: name of the test and optional category (defaults to "General"). Then all required steps should be added to the test instance.

To add a step to the test, the ``addStep(description, function=None, prestep=None, isVerifyStep=False)`` method is used. It accepts four parameters: *description*, *function*, *prestep*, *isVerifyStep*.

The first one is mandatory and is a string with the description of the step. The second one is optional and should be a function. If this parameters is passed, the function will be executed at that step, and it will be an automated step. If no function is passed, the step will be considered a manual one. The description will be shown to the user and he will perform the step manually.

If once the manual step has been performed, the tester has to verify something, the *isVerifyStep* parameter should be *True*. That will cause the "Step passes" and "Step fails" buttons to be active, instead of the simple "Next step" one.

If you require some preparation routine to be executed before actually entering this step, pass the corresponding function using the ``prestep`` parameter.

You can add a cleanup task to be performed when the test is finished (or skipped), by using the ``setCleanup()`` method  of the *Test* class and passing a function where the cleanup is to be performed.

Tests can have associated issue URL, it is defined using the ``setIssueURL()`` method of the *Test* class, in case you are using a testing platform to keep track of test executions. If issue URL is defined user can open corresponding page from the test context menu in the test report dialog.
