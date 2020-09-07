.. (c) 2016 Boundless, http://boundlessgeo.com
   This code is licensed under the GPL 2.0 license.

Usage
=====

This section explains how to execute tests using the tester plugin.


Running tests
#############

To start a test cycle, select the :menuselection:`Plugins --> Tester --> Start testing` menu.

The :guilabel:`Test selector` window will be shown with the available tests grouped by plugin and categories.

.. image:: testselector.png
	:align: center

The list of available tests depends on the active plugins. The Tester plugin itself contains no tests, except for a few metatests. Other tests are added by plugins when they are loaded.

.. tip::

   If a plugin is active, but its tests are not available in the Tester plugin, it might be because it was activated before the Tester plugin was loaded. Try disabling and enabling the plugin to add its tests again, and then reopen the Tester plugin test selector.

Select the tests that you want to be executed and then click :guilabel:`Run selected tests`.

In the upper part of the QGIS map canvas, you will see the guilabel:`Tester plugin` panel.

.. image:: testpanel_upload_dragdrop.png
	:align: center

It has a single panel with a description of the current step in the current test. If the step is automated (that is, if no user interaction is expected during this step), the panel is disabled. Otherwise, the panel will show a description of the task that the test expects you to perform.

All tests selected in the test selection dialog will be run sequentially. Tests can be of two types: automated and semi-automated. Each of them is described in the next sections, with indications about how to run the test in each case.

Automated tests
----------------

Automated tests have no user interaction. The Tester plugin will take care of running the test and checking that the conditions defined to pass the test are met.


Semi-automated tests
---------------------

Semi-automated tests contain steps that do not require user interaction (such as data preparation), along with steps that require the user to perform a given task or to check that the result of a previous step is correct.

Here are a couple of examples of such tests, to help understand how the user should interact with the plugin in these cases.

**Example 1**: A test to check the correct uploading of styles to a GeoServer catalog
.....................................................................................

It has the following steps:

- Open a QGIS project and upload one of its layers (including its style) to a test GeoServer catalog
- Create a WMS layer that connects to the layer uploaded to GeoServer on the previous step
- Verify that the rendering of the WMS layer matches that of the original vector layer

The two first steps are automated, the user doesn't have to do anything. At the end of those steps, the project will have a vector layer with a symbology stored in the project, and a WMS layer with a symbology that is used client-side.

The third step is manual, and the test panel will show something like this.

.. image:: testpanel_verify_rendering.png
	:align: center

It tells the user to verify that symbology is correctly uploaded and used. Based on that, the user should indicate whether the :guilabel:`Test passes` or :guilabel:`Test fails`. Once the user clicks on any of the buttons to indicate that, the test is finished and the plugin will move to the next test.

**Example 2**: A test to verify that a layer is correctly imported into GeoServer by dragging and dropping
..........................................................................................................

It has the following steps:

- Create a GeoServer catalog and set it up in the GeoServer explorer plugin. Open the GeoServer explorer.
- Drag a layer file from the QGIS browser into the item corresponding to that catalog in the GeoServer explorer
- Verify that a layer has been created in the GeoServer catalog

In this case, the first step is automated. It leaves QGIS and GeoServer ready for the next step, which has to be performed by the user.

The test panel will look like this.

.. image:: testpanel_upload_dragdrop.png
	:align: center

Since this is not the final step, the :guilabel:`Test passes` and :guilabel:`Test fails` buttons are disabled. Instead, a :guilabel:`Next step` button is enabled. The user should click it once he has performed the task indicated in the panel (in this case, once the layer file has been dragged into the GeoServer explorer)

The last step is automated. The plugin will decide if the test passes or not, by checking the layers in the catalog. The user interaction is not needed for that. Once checked, the plugin will move to the next test.

Some tests might contain intermediate manual steps where something is to be verified by the user. In this case, the :guilabel:`Test passes` and :guilabel:`Test fails` buttons will be renamed to :guilabel:`Step passes` and :guilabel:`Step fails` and will be enabled.

At any time, the user can click :guilabel:`Skip test` to cancel the current test and move to the next one, or click :guilabel:`Cancel testing` to skip the remaing tests and show the :guilabel:`Test report`.

Test report
#############

Once all the selected tests have been run (or skipped), the test panel is hidden and a test results dialog is shown.

.. image:: testresults.png
	:align: center

For those tests that have not passed correctly (displayed in red), you can click on their names and a detailed error trace will be shown in the lower panel

.. image:: testresulttrace.png
	:align: center

Right-clicking on the test name in the list will open a context menu with a single menu entry: "Open issue page". Select it to open the corresponding issue page for the test, in case it has been defined. If no issue page has been defined for that test, the context menu will not be shown.
