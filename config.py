# -*- coding: utf-8 -*-

# Server address
HOST = "127.0.0.1"
PORT = 3000
# Server messages
# Zpráva s potvrzovacím kódem. Může obsahovat maximálně 5 čísel a ukončovací sekvenci \a\b.
# SERVER_CONFIRMATION = "#<16-bitové číslo v decimální notaci>\a\b"
# Příkaz pro pohyb o jedno pole vpřed
SERVER_MOVE = "102 MOVE\a\b"
# Příkaz pro otočení doleva
SERVER_TURN_LEFT = "103 TURN LEFT\a\b"
# Příkaz pro otočení doprava
SERVER_TURN_RIGHT = "104 TURN RIGHT\a\b"
# Příkaz pro vyzvednutí zprávy
SERVER_PICK_UP = "105 GET MESSAGE\a\b"
# Příkaz pro ukončení spojení po úspěšném vyzvednutí zprávy
SERVER_LOGOUT = "106 LOGOUT\a\b"
# Kladné potvrzení
SERVER_OK = "200 OK\a\b"
# Nezdařená autentizace
SERVER_LOGIN_FAILED = "300 LOGIN FAILED\a\b"
# Chybná syntaxe zprávy
SERVER_SYNTAX_ERROR = "301 SYNTAX ERROR\a\b"
# Zpráva odeslaná ve špatné situaci
SERVER_LOGIC_ERROR = "302 LOGIC ERROR\a\b"

# Client messages
# Zpráva s uživatelským jménem. Jméno může být libovolná sekvence znaků kromě kromě dvojice \a\b.
# CLIENT_USERNAME = "<user name>\a\b"
CLIENT_USERNAME_MAX_LEN = 12 - 2    # - 2 chars, \a\b
# Zpráva s potvrzovacím kódem. Může obsahovat maximálně 5 čísel a ukončovací sekvenci \a\b.
# CLIENT_CONFIRMATION = "<16-bitové číslo v decimální notaci>\a\b"
CLIENT_CONFIRMATION_MAX_LEN = 7 - 2
# Potvrzení o provedení pohybu, kde x a y jsou souřadnice robota po provedení pohybového příkazu.
# CLIENT_OK = "OK <x> <y>\a\b"
CLIENT_OK_MAX_LEN = 12 - 2
# Robot se začal dobíjet a přestal reagovat na zprávy.
CLIENT_RECHARGING = "RECHARGING\a\b"
CLIENT_RECHARGING_MAX_LEN = 12 - 2
# Robot doplnil energii a opět příjímá příkazy.
CLIENT_FULL_POWER = "FULL POWER\a\b"
CLIENT_FULL_POWER_MAX_LEN = 12 - 2
# Text vyzvednutého tajného vzkazu. Může obsahovat jakékoliv znaky kromě ukončovací sekvence \a\b.
# CLIENT_MESSAGE = <text>\a\b
CLIENT_MESSAGE_MAX_LEN = 100 - 2

# Time constants
# Server i klient očekávají od protistrany odpověď po dobu tohoto intervalu.
TIMEOUT = 1
# Časový interval, během kterého musí robot dokončit dobíjení.
TIMEOUT_RECHARGING = 5

# Authentication keys
SERVER_KEY = 54621
CLIENT_KEY = 45328

# Other constants
GOAL_LOCATION = (0, 0)
UNINITIALIZED = -1
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
