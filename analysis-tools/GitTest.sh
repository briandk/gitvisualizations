mkdir newProject
cd newProject
git init
echo 'hello, world!' >> testFile.txt
git add testFile.txt
git commit -m "Initial Commit"
git blame testFile.txt

echo 'hello again!' >> testFile.txt
git add testFile.txt
git commit -m "Initial Commit"
git blame testFile.txt