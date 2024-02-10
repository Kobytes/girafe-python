# GIRAFE : Générateur d'Interfaces Réseaux Automatisé Facile et Efficace
# Script pour la configuration d'un switch Cisco

# Mise à jour du script pour demander les données à l'utilisateur

def configurer_nom_hote():
    nom_hote = input("Entrez le nom d'hôte du switch: ")
    return f"hostname {nom_hote}\n"

def configurer_acces_securise():
    mot_de_passe_exec = input("Entrez le mot de passe pour l'Exec Mode: ")
    mot_de_passe_console = input("Entrez le mot de passe pour l'accès console: ")
    mot_de_passe_vty = input("Entrez le mot de passe pour l'accès VTY (SSH/Telnet): ")

    config = f"""
enable secret {mot_de_passe_exec}
line console 0
 password {mot_de_passe_console}
 login
line vty 0 4
 password {mot_de_passe_vty}
 login
    """
    return config

def configurer_vlans():
    vlans_config = {}
    nombre_vlans = int(input("Combien de VLANs souhaitez-vous configurer? "))
    for _ in range(nombre_vlans):
        vlan_id = input("Entrez l'ID du VLAN: ")
        nombre_ports = int(input(f"Combien de ports pour le VLAN {vlan_id}? "))
        vlans_config[vlan_id] = [input(f"Entrez le numéro du port {i+1} pour le VLAN {vlan_id}: ") for i in range(nombre_ports)]
    return vlans_config

def configurer_agregation_liens():
    lags_config = {}
    nombre_lags = int(input("Combien de groupes d'agrégation de liens (LAGs) souhaitez-vous configurer? "))
    for _ in range(nombre_lags):
        lag_id = input("Entrez l'ID du LAG: ")
        nombre_ports = int(input(f"Combien de ports pour le LAG {lag_id}? "))
        lags_config[lag_id] = [input(f"Entrez le numéro du port {i+1} pour le LAG {lag_id}: ") for i in range(nombre_ports)]
    return lags_config

def configurer_stp():
    mode_stp = input("Entrez le mode STP (pvst, rapid-pvst, mstp, etc.): ")
    priorite_pont = input("Entrez la priorité du pont pour le STP: ")
    return f"spanning-tree mode {mode_stp}\nspanning-tree vlan 1 priority {priorite_pont}\n"

def configurer_adresse_ip_gestion():
    vlan_id = input("Entrez l'ID du VLAN pour la gestion à distance: ")
    ip_adresse = input("Entrez l'adresse IP pour la gestion à distance: ")
    subnet_mask = input("Entrez le masque de sous-réseau: ")

    return f"vlan {vlan_id}\ninterface vlan {vlan_id}\nip address {ip_adresse} {subnet_mask}\nno shutdown\n"

def activer_interfaces_utilisees(vlans_config):
    config = ""
    tous_ports = {port for ports in vlans_config.values() for port in ports}
    for port in tous_ports:
        config += f"interface FastEthernet{port}\n no shutdown\n"
    return config

def desactiver_interfaces_non_utilisees(vlans_config, nombre_total_interfaces=24):
    config = ""
    tous_ports_utilises = {port for ports in vlans_config.values() for port in ports}
    for i in range(1, nombre_total_interfaces + 1):
        port = f"0/{i}"
        if port not in tous_ports_utilises:
            config += f"interface FastEthernet{port}\n shutdown\n"
    return config

def activer_ssh():
    nom_domaine = input("Entrez le nom de domaine pour la configuration SSH: ")
    taille_cle_rsa = input("Entrez la taille de la clé RSA (par exemple, 1024 ou 2048): ")

    config = f"""
ip domain-name {nom_domaine}
crypto key generate rsa modulus {taille_cle_rsa}
ip ssh version 2
    """
    return config

def generer_config_globale():
    config = configurer_nom_hote()
    config += configurer_acces_securise()
    vlans_config = configurer_vlans()
    config += configurer_vlans(vlans_config)
    config += activer_interfaces_utilisees(vlans_config)
    config += desactiver_interfaces_non_utilisees(vlans_config)
    lags_config = configurer_agregation_liens()
    config += configurer_agregation_liens(lags_config)
    config += configurer_stp()
    config += configurer_adresse_ip_gestion()
    config += activer_ssh()

    return config

# Génération de la configuration globale
config_complete_globale = generer_config_globale()
print(config_complete_globale)
