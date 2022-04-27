import click
import notion
from cryptography.fernet import Fernet
from decouple import config

@click.group()
def cli():
    pass

@cli.command()
@click.option("--sito", prompt="Sito del quale si vuole salvare le credenziali", help="Il sito o app di cui salvare le credenziali")
@click.option("--user", prompt="User", help="User da salvare")
@click.option("--password", prompt="Password", hide_input=True, confirmation_prompt=True, help="Password da salvare")
def newPassword(sito, user, password):
    """Comando per la creazione di una nuova password"""
    click.echo(f"Sito: {sito} - User: {user} - Password: {password}")
    encrypted_psw = encrypt(password)
    result = notion.aggiungiPagina(sito, user, encrypted_psw)
    click.echo(f"{result}")

@cli.command()
@click.option("--sito", default=None, help="Se viene passato il parametro mostra le credenziali per quel sito")
def getPassword(sito):
    """Comando per la visualizzazione delle password. Se viene passato il parametro mostra quelle del sito indicato"""
    data = notion.getPasswords(sito)
    
    if not data:
        click.echo(f"Non esitostono credenziali salvate")
    else:
        for credential in data:
            click.echo("-------------------------------------------------------------------------------")
            click.echo(f"Sito: {credential['properties']['Site']['title'][0]['text']['content']}")
            click.echo(f"User: {credential['properties']['User']['rich_text'][0]['text']['content']}")
            click.echo(f"Password: {decrypt(credential['properties']['Password']['rich_text'][0]['text']['content'])}")
            click.echo("-------------------------------------------------------------------------------")

def load_key():
    return config('SECRET_KEY')

def encrypt(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    return f.encrypt(encoded_message)

def decrypt(encrypted_message):
    key = load_key()
    f = Fernet(key)
    encrypted_message_byte = encrypted_message.encode()
    return f.decrypt(encrypted_message_byte)

if __name__ == '__main__':
    cli()
