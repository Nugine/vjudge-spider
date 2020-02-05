# vjudge-spider

a toy spider for data preprocess

get data from contest/123456:

```bash
echo "my-username" > account.txt
echo "my-password" >> account.txt
python3 -m vjspd 123456 -a account.txt -o 123456.json
```

or

```bash
python3 -m vjspd 123456 -u "my-username" -p "my-password" > 123456.json
```