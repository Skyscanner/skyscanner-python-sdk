=======================================
Contributing to Skyscanner's Python SDK
=======================================

We're glad you want to make a contribution!

Fork this repository and send in a pull request when you're finished with your changes. Link any relevant issues in too.

Take note of the build status of your pull request, only builds that pass will be accepted. Please also keep to our conventions and style so we can keep this repository as clean as possible.

License
-------

By contributing your code, you agree to license your contribution under the terms of the APLv2: https://github.com/Skyscanner/skyscanner-python-sdk/blob/master/LICENSE.md

All files are released with the Apache 2.0 license.

If you are adding a new file it should have a header like this:

    /**

    * Copyright 2015 Skyscanner Limited.

    *

    * Licensed under the Apache License, Version 2.0 (the "License");

    * you may not use this file except in compliance with the License.

    * You may obtain a copy of the License at

    * * http://www.apache.org/licenses/LICENSE-2.0

    *

    * Unless required by applicable law or agreed to in writing, software * distributed under the License is distributed on an "AS IS" BASIS,

    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

    * See the License for the specific language governing permissions and * limitations under the License.

    */

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/Skyscanner/skyscanner-python-sdk/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Skyscanner Python SDK could always use more documentation, whether as part of the
official Skyscanner Python SDK docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/Skyscanner/skyscanner-python-sdk/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `skyscanner` for local development.

1. Fork the `skyscanner` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/skyscanner-python-sdk.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv skyscanner
    $ cd skyscanner/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 skyscanner tests
    $ python setup.py test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, 3.3, and 3.4, and for PyPy. Check
   https://travis-ci.org/Skyscanner/skyscanner-python-sdk/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ python -m unittest tests.test_skyscanner