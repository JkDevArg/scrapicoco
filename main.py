from bs4 import BeautifulSoup
import webbrowser
import sys
import re
import requests
from requests.exceptions import RequestException
import time
from datetime import datetime

def main_menu():
    while True:
        print("Security Recon App Proxy")
        print("1. Configurar target")
        print("2. Github")
        print("3. Linkedin")
        print("4. Salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            configure_target()
        elif choice == '2':
            webbrowser.open('https://github.com/JkDevArg')
        elif choice == '3':
            webbrowser.open('https://www.linkedin.com/in/joaquincenturion/')
        elif choice == '4':
            sys.exit()
        else:
            print("Opción no válida, por favor intente nuevamente.")

def configure_target():
    target_url = input("Ingrese la URL del target: ")
    # Ensure target_url starts with http:// or https://
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    secondary_menu(target_url)

def secondary_menu(target_url):
    while True:
        print("\nMenú de opciones")
        print("1. Buscar correos")
        print("2. Buscar teléfonos")
        print("3. Buscar enlaces")
        print("4. Servicios de terceros")
        print("5. Atrás")

        choice = input("Seleccione una opción: ")

        if choice in ['1', '2', '3', '4']:
            use_proxy = input("¿Usará un proxy? (S/N): ").upper()
            proxies = None
            if use_proxy == 'S':
                proxy_source = input("Seleccione la fuente de proxies (A: Archivo, I: Internet, N: Ninguno): ").upper()
                if proxy_source == 'A':
                    proxy_file = input("Ingrese la ubicación del archivo de proxies: ")
                    proxies = load_proxies(proxy_file)
                elif proxy_source == 'I':
                    download_proxies("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", "proxy.txt")
                    proxies = load_proxies("proxy.txt")
                elif proxy_source == 'N':
                    pass
                else:
                    print("Opción no válida. No se utilizará un proxy.")
            perform_action(choice, target_url, proxies)
        elif choice == '5':
            return
        else:
            print("Opción no válida, por favor intente nuevamente.")

def save_to_file(data, data_type, target_url, proxy_used=None):
    # Formatear la fecha actual
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # Generar el nombre del archivo
    domain = target_url.replace('https://', '').replace('http://', '').replace('/', '_')
    filename = f"{domain}-{data_type}-{now}.txt"

    with open(filename, 'w') as file:
        for item in data:
            if proxy_used:
                file.write(f"{item} - proxy sí: {proxy_used}\n")
            else:
                file.write(f"{item} - proxy no\n")
    print(f"Datos guardados en {filename}")

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def download_proxies(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'w') as file:
            file.write(response.text)
        print(f"[+] Proxies descargados y guardados en {filename}")
    except RequestException as e:
        print(f"[-] Error al descargar proxies: {e}")

def perform_action(choice, target_url, proxies):
    if choice == '1':
        find_emails(target_url, proxies)
    elif choice == '2':
        find_phones(target_url, proxies)
    elif choice == '3':
        find_links(target_url, proxies)
    elif choice == '4':
        find_third_party_services(target_url, proxies)

def fetch_page_content(url, proxies_list):
    timeout = 15  # Tiempo de espera en segundos
    if proxies_list is None:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Lanzar una excepción para códigos de estado HTTP 4xx/5xx
            return response.text, None  # No se usó proxy
        except RequestException as e:
            print(f"[-] Error al recuperar la página sin proxy: {e}")
            return None, None
    else:
        for proxy in proxies_list:
            proxy_dict = {'http': proxy, 'https': proxy}
            try:
                response = requests.get(url, proxies=proxy_dict, timeout=timeout)
                print(f"[+] Usando proxy: {proxy}")  # Imprimir el proxy usado
                return response.text, proxy
            except RequestException as e:
                print(f"[-] Proxy {proxy} error. Probando el siguiente proxy...")
                time.sleep(1)  # Esperar un segundo antes de intentar el siguiente proxy

        # Si todos los proxies fallaron
        print("Todos los proxies fallaron. No se pudo recuperar la página.")
        return None, None

def find_emails(target_url, proxies):
    content, proxy_used = fetch_page_content(target_url, proxies)
    if content is None:
        return  # No se pudo recuperar el contenido

    soup = BeautifulSoup(content, 'html.parser')
    emails = set()

    # Buscar correos electrónicos en los enlaces mailto:
    for a in soup.find_all('a', href=True):
        if 'mailto:' in a['href']:
            email = a['href'].split(':')[1]
            emails.add(email)

    # Buscar correos electrónicos en el texto del contenido
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    for text in soup.stripped_strings:
        found_emails = email_pattern.findall(text)
        for email in found_emails:
            emails.add(email)

    if emails:
        save_data = input("¿Desea guardar los correos encontrados? (S/N): ").upper()
        if save_data == 'S':
            save_to_file(emails, 'email', target_url, proxy_used)
    else:
        print("No se encontraron datos")

def find_phones(target_url, proxies):
    content, proxy_used = fetch_page_content(target_url, proxies)
    if content is None:
        return  # No se pudo recuperar el contenido

    soup = BeautifulSoup(content, 'html.parser')
    phones = set()

    for text in soup.stripped_strings:
        if text.startswith('+') and text[1:].isdigit():
            phones.add(text)

    if phones:
        save_data = input("¿Desea guardar los teléfonos encontrados? (S/N): ").upper()
        if save_data == 'S':
            save_to_file(phones, 'phone', target_url, proxy_used)
    else:
        print("No se encontraron datos")

def find_links(target_url, proxies):
    content, proxy_used = fetch_page_content(target_url, proxies)
    if content is None:
        return  # No se pudo recuperar el contenido

    soup = BeautifulSoup(content, 'html.parser')
    links = set(a['href'] for a in soup.find_all('a', href=True))

    if links:
        save_data = input("¿Desea guardar los enlaces encontrados? (S/N): ").upper()
        if save_data == 'S':
            save_to_file(links, 'link', target_url, proxy_used)
    else:
        print("No se encontraron datos")

def find_third_party_services(target_url, proxies):
    content, proxy_used = fetch_page_content(target_url, proxies)
    if content is None:
        return  # No se pudo recuperar el contenido

    soup = BeautifulSoup(content, 'html.parser')
    services = set()

    for script in soup.find_all('script', src=True):
        services.add(script['src'])
    for link in soup.find_all('link', href=True):
        services.add(link['href'])

    if services:
        save_data = input("¿Desea guardar los servicios de terceros encontrados? (S/N): ").upper()
        if save_data == 'S':
            save_to_file(services, 'third-party-services', target_url, proxy_used)
    else:
        print("No se encontraron datos")

if __name__ == "__main__":
    main_menu()
