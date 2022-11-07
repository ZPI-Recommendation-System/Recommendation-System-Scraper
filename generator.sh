git pull
sqlacodegen postgresql://backend:backend123@localhost:5035/recommendation-system > db/entities.py
git add db/entities.py
git commit -m "Automatic Entity Upgrade"
git push
