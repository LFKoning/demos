import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _(pd):
    # Define some dummy names.
    df = pd.DataFrame({
        "names": ["Mark Jansen", "Ingrid de Boer"]
    })
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hashing
    """)
    return


@app.cell
def _(sha_hash):
    # Simply hash the value using SHA256.
    sha_hash("Mark Jansen")
    return


@app.cell
def _(generate_salt):
    # Generate a random salt.
    salt = generate_salt()
    salt
    return (salt,)


@app.cell
def _(salt, sha_hash):
    # Hash the name including a salt
    # Note: Returns a different hash.
    sha_hash("Mark Jansen", salt=salt)
    return


@app.cell
def _(df, generate_salt):
    hashed = df.assign(salt=generate_salt())
    hashed
    return (hashed,)


@app.cell
def _(hashed, sha_hash):
    # Add hashed values.
    hashed["hash"] = hashed.apply(
        lambda row: sha_hash(value=row["names"], salt=row["salt"]),
        axis=1,
    )

    hashed
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Encryption
    """)
    return


@app.cell
def _(aes_generate_key):
    # Generate a unique encryption key.
    key = aes_generate_key()
    key
    return (key,)


@app.cell
def _(aes_encrypt, key):
    cypher = aes_encrypt("Mark Jansen", key)
    cypher
    return (cypher,)


@app.cell
def _(aes_decrypt, cypher, key):
    aes_decrypt(cypher, key)
    return


@app.cell
def _(aes_encrypt, df, key):
    encrypted = df.assign(encrypted=df["names"].map(lambda n: aes_encrypt(n, key)))
    encrypted
    return (encrypted,)


@app.cell
def _(encrypted):
    encrypted.to_csv("test_encryption.csv", index=False)
    return


@app.cell
def _(pd):
    pd.read_csv("test_encryption.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Imports and functions
    """)
    return


@app.cell
def _():
    import uuid
    import string

    from hashlib import sha256
    from secrets import token_bytes

    import marimo as mo
    import pandas as pd

    from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
    return AESGCMSIV, mo, pd, sha256, token_bytes, uuid


@app.cell
def _(AESGCMSIV, sha256, token_bytes, uuid):
    def sha_hash(value: str, salt: str = None, encoding="utf8") -> str:
        """Hash a string value using SHA256 with optional salt.

        Parameters
        ----------
        value : str
            Value to hash.
        salt : str, optional
            String to use as a salt.
        encoding : str, default="utf8"
            Encoding converting strings into bytes.

        Returns
        -------
        str
            Hashed value as a string.
        """
        if isinstance(salt, str):
            value = salt + value

        hashed = sha256(value.encode(encoding))
        return hashed.hexdigest()


    def generate_salt() -> str:
        """Generate a random UUID salt for hashing."""
        return uuid.uuid4().hex


    def aes_encrypt(value: str, key: bytes, encoding="utf8") -> bytes:
        """Encrypt a string value using AES-GCMS-SIV encryption.

        Parameters
        ----------
        value : str
            Value to encrypt as string.
        encoding : str, default="utf8"
            Encoding for converting strings into bytes.

        Returns
        -------
        str
            Encrypted value as a string.
        """
        value = value.encode(encoding)

        # Generate a 12 byte nonce.
        # Note: Not 100% garantueed to be unique!
        nonce = token_bytes(12)

        encryptor = AESGCMSIV(key)
        cypher = encryptor.encrypt(nonce, value, b"")
        return nonce + cypher


    def aes_decrypt(cypher: bytes, key: bytes, encoding="utf8") -> str:
        """Decrypt a string value using AES-GCMS-SIV encryption.

        Parameters
        ----------
        cypher : str
            Encrypted value as string.
        encoding : str, default="utf8"
            Encoding converting strings into bytes.

        Returns
        -------
        str
            Encrypted value as a string.
        """
        nonce = cypher[0:12]
        encryptor = AESGCMSIV(key)
        return encryptor.decrypt(nonce, cypher[12:], b"").decode(encoding)


    def aes_generate_key(bit_length: int = 128) -> bytes:
        """Generate an AES-GCM-SIV compatitble encryption key.

        Parameters
        ----------
        bit_length : int, default=128
            Length of the key in bytes.

        Returns
        -------
        bytes
            The generated AES-GCM IV key.
        """
        return AESGCMSIV.generate_key(bit_length=bit_length)
    return aes_decrypt, aes_encrypt, aes_generate_key, generate_salt, sha_hash


@app.cell
def _():
    return


@app.cell
def _():
    import yaml
    from typing import Self
    from pydantic import BaseModel


    class Item(BaseModel):
        name: str
        children: list[Self] | None = None


    class ItemList(BaseModel):
        items: list[Item]
        names: list = []

        def _extract_names(self, item: Item):
            self.names.append(item.name)

            if item.children:
                for child in item.children:
                    self._extract_names(child)

        def model_post_init(self, _):
            for item in self.items:
                self._extract_names(item)



    items = """
    items:
    - name: GrandParent1
      children:
        - name: TestParent1.1
          children:
            - name: TestChild1.1.1
            - name: TestChild1.1.2

    - name: TestParent2
      children:
        - name: TestChild2.1
        - name: TestChild2.2
    """

    ItemList.model_validate(yaml.safe_load(items)).model_dump()
    return


if __name__ == "__main__":
    app.run()
