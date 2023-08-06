kpctl
=====

Command line interface to:

- inspect, document, enhance and validate BPMN files; and
- execute process-based applications on the KnowProcess platform

Build and publish to Test version of PyPI
-----------------------------------------

1. Increment version

   ```
   bumpversion --current-version 3.1.0 [major|minor|patch] setup.py kpctl/__init__.py
   ```

2. Build...

   ```
   python3 setup.py sdist bdist_wheel
   ```

3. Check (note this is not exhaustive)

   ```
   twine check dist/*
   ```

4. Publish to test server (can be repeated for same version)

   ```
   twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```
