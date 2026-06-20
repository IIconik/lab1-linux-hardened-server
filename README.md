# Lab 1 — Linux Hardened Server

> Mise en place complète d'un serveur Ubuntu 22.04 LTS sécurisé pour la production.
> Premier lab du parcours **Cloud Infrastructure Engineer** (Phase 0 — Socle Technique).

[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04_LTS-E95420?logo=ubuntu&logoColor=white)]()
[![Status](https://img.shields.io/badge/Status-Validated-3FB950)]()
[![Lab](https://img.shields.io/badge/Lab-Phase_0-58A6FF)]()

---

## 🎯 Objectif

Déployer un serveur Linux durci de bout en bout, prêt à accueillir des services en production. L'accent est mis sur la sécurité par défaut, la défense en profondeur et l'automatisation des tâches de monitoring.

## 🛠️ Ce qui est mis en place

| Composant | Configuration |
|-----------|--------------|
| **Réseau** | IP statique via Netplan (renderer: networkd) |
| **Utilisateurs** | Compte sudo + utilisateur `deployer` sans shell |
| **SSH** | Port 222, auth par clé uniquement, MaxAuthTries 2 |
| **Firewall** | UFW avec règles minimalistes (deny-all par défaut) |
| **Anti brute-force** | Fail2Ban avec `banaction = ufw` |
| **Monitoring** | Service systemd Python loggant CPU/RAM/Disk/SSH toutes les 5 min |
| **Rotation logs** | Logrotate hebdomadaire avec compression |

## 📋 Prérequis

- VirtualBox (ou tout hyperviseur)
- ISO Ubuntu Server 22.04 LTS
- Accès réseau en mode bridge (pour avoir une IP sur le LAN)
- 2 vCPU, 2 GB RAM minimum, 10 GB disque

## 🚀 Déploiement

La procédure complète et détaillée est disponible dans le PDF :

📄 **[Lab1_Linux_Hardened_Server.pdf](./Lab1_Linux_Hardened_Server.pdf)**

Elle couvre les 8 chapitres suivants :

1. Configuration réseau (Netplan)
2. Utilisateurs et droits
3. Sécurisation SSH
4. Firewall UFW
5. Protection brute-force (Fail2Ban)
6. Service systemd d'audit
7. Rotation des logs (Logrotate)
8. Validation finale

## 📁 Structure du repo

```
lab1-linux-hardened-server/
├── README.md                              ← ce fichier
├── Lab1_Linux_Hardened_Server.pdf         ← procédure complète
├── configs/
│   ├── netplan/00-installer-config.yaml   ← config réseau
│   ├── ssh/sshd_config                    ← config SSH durcie
│   ├── ufw/                               ← règles UFW
│   ├── fail2ban/jail.local                ← config Fail2Ban
│   └── logrotate/audit                    ← rotation des logs
├── scripts/
│   └── audit.py                           ← script d'audit système
└── systemd/
    └── log-python.service                 ← unit file systemd
```

## ✅ Validation

Le serveur est considéré comme opérationnel quand :

- [x] `ping 8.8.8.8` et `ping archive.ubuntu.com` répondent
- [x] La connexion SSH au port 22 est refusée
- [x] La connexion SSH au port 222 par clé fonctionne
- [x] `sudo ufw status` affiche les 4 règles attendues
- [x] `sudo fail2ban-client status sshd` affiche la jail active
- [x] `sudo systemctl status log-python` retourne `active (running)`
- [x] `tail /var/log/audit.log` affiche les métriques toutes les 5 min

## 🔍 Tests effectués

- Test de ban Fail2Ban : 3 tentatives SSH échouées → IP bannie via UFW pendant 2h
- Test de redémarrage : tous les services se relancent automatiquement
- Test logrotate : `sudo logrotate -d` sans erreur
- Test du service d'audit : entrées générées toutes les 5 minutes confirmées

## 📚 Erreurs rencontrées et solutions

| Erreur | Solution |
|--------|----------|
| `NetworkManager.service not found` | Remplacer `renderer: NetworkManager` par `renderer: networkd` |
| `action.d/ufw-multiport non trouvé` | Vider `/etc/fail2ban/jail.d/defaults-debian.conf` |
| Bans Fail2Ban inefficaces | Ajouter `banaction = ufw` dans `jail.local` |
| Ban après 5 tentatives au lieu de 3 | Ajouter `MaxAuthTries 2` dans `sshd_config` |

## 🎓 Compétences mises en pratique

- Administration système Linux (Ubuntu Server)
- Configuration réseau (Netplan, systemd-networkd)
- Sécurité serveur (SSH hardening, UFW, Fail2Ban)
- Création de services systemd
- Scripting Python pour l'infra
- Gestion des logs (journald, logrotate)

## 🔜 Prochaine étape

**Lab 2 — Bash Monitoring** : créer un script de monitoring complet avec alertes Slack et rapport JSON.

À terme : automatiser l'intégralité de cette configuration via **Ansible** pour pouvoir provisionner 10 serveurs identiques en une commande.

---

**Parcours :** BTS SIO SISR → Bachelor ESGI Cloud/Réseaux → Mastère
**Objectif :** Cloud Infrastructure / Platform Engineer
