# Building the Package

> Versions are always of the form `X.X.X`.

## Testing
Before uploading the package to a live server, first check that it uploads corectly.

1. Update the version in `setup.py`.
2. After creating and testing the package functionality, [prepare it for upload](https://stackoverflow.com/questions/6323860/sibling-package-imports/50193944#50193944) to [PyPi](https://pypi.org/) using
```bash
python setup.py sdist bdist_wheel
```
3. Check the `README.rst` using `twine check dist/*`.
4. Upload it to the test server `twine upload -r pypitest dist/*<version>*`.
5. Install the test version with
``` bash
pip install --index-url https://test.pypi.org/simple/ <package name>
```
6. Remove any unneeded verison in the `dist/` folder.

## Making It Live
1. Commit the changes.
	1. Commit the changes on git.
	2. Tag the commit with the new version `git tag v<version>`. 
	3. Merge with `master` branch.
2. Upload to PyPi using `twine upload -r pypi dist/*<version>*`
3. Upload to GitHub.