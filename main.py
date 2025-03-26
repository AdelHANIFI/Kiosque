
import sys
import resources_rc
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QComboBox, QStackedWidget
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, Signal
from dons_page import DonsPage
from ramadan_page import RamadanPage
from iftar_page import IftarPage  
from zakat_page import ZakatPage
from work_page import WorksPage
from otheramount_page import OtherAmountPage
from payment_page import PaymentPage
from splash_page import SplashPage
from home_page import HomePage  


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        app.setAttribute(Qt.AA_EnableHighDpiScaling)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)
        self.setWindowTitle("Borne de Paiement - Mosquée de Pau")
        self.showFullScreen()  # Fenêtre en plein écran


        self.sumup_api_key = "sup_sk_YkWjlUS5edcb0LAVsObRwsJXJu9dMyH6o"  # Remplacez par votre clé API
        self.merchant_code = "MFT77XNQ"  # Remplacez par votre code marchand
        self.pairing_code = "EZRVUID3R"  # Remplacez par le code de pairing affiché sur le terminal


        # Traductions
        self.current_language = "fr"
        self.translations = self.load_translations()


        # Créer un gestionnaire de pages
        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)


        # Charger le fichier de styles
        self.apply_styles()

        # Ajouter les pages
        self.splash_page = SplashPage(self.pages, self.translations, self.current_language)
        self.splash_page.language_changed.connect(self.change_language)
        self.home_page = HomePage(self.pages, self.translations, self.current_language)
        self.payment_page = PaymentPage(self.pages)
        self.dons_page = DonsPage(self.pages, self.payment_page, self.translations, self.current_language)
        self.ramadan_page = RamadanPage(self.pages, self.translations, self.current_language)
        self.iftar_page = IftarPage(self.pages, self.payment_page, self.translations, self.current_language)
        self.zakat_page = ZakatPage(self.pages, self.payment_page, self.translations, self.current_language)
        self.works_page = WorksPage(self.pages, self.payment_page ,self.translations, self.current_language)
        self.otheramount_page = OtherAmountPage(self.pages, self.payment_page, self.translations, self.current_language)

        self.pages.addWidget(self.splash_page)  # index 0
        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.payment_page)
        self.pages.addWidget(self.dons_page)
        self.pages.addWidget(self.ramadan_page)
        self.pages.addWidget(self.iftar_page)
        self.pages.addWidget(self.zakat_page)
        self.pages.addWidget(self.works_page)
        self.pages.addWidget(self.otheramount_page)

        self.pages.setCurrentWidget(self.splash_page)  # Démarrer sur la page d'accueil
    def load_translations(self):
        """
        Charge les traductions.
        """
        return {
            "fr": {
                "title": "Je soutiens la Mosquée de Pau",
                "splash_title": "Borne de Paiement",
                "splash_instruction": "Cliquez n'importe où pour continuer",
                "adherents": "Espace Adhérents",
                "adherents_help": "Rechargez votre carte d'adhérent",
                "coming_soon": "Bientôt disponible",
                "mosque": "Dons pour le projet de la mosquée",
                "mosque_help": "Aidez la mosquée à construire un parking",
                "works": "Travaux de la mosquée",
                "works_help": "Soutenez les rénovations et les projets",
                "ramadan": "Ramadan",
                "ramadan_help": "Dons pour l'Iftar et la Zakât al-Fitr",
                "ramadan_title": "Dons pour le Ramadan",
                "sadaqa_button": "Faire une Sadaqa pour l'Iftar",
                "footer": "Edited by @adelhanifi",
                "language_label": "Langue",
                "other_amount": "Autre\nmontant",
                "other_amount_title": "Saisissez un montant",
                "hide_amount": "Cacher Montant",
                "show_amount": "Afficher Montant",
                "validate": "Valider",
                "back": "Retour",
                "invalid_amount": "Veuillez entrer un montant valide.",
                "zakat": "payez 7€",
                "zakat_title": "Zakât al-Fitr",
                "zakat_explanation": "La Zakât al-Fitr est fixée à 7 € par personne.\nVeuillez appuyer sur le bouton ci-dessous pour la payer.",
                "zakat_button": "Payer la Zakat al-Fitr (7 €)",
                "payment_title": "JE SOUTIENS",
                "payment_subtitle": "Mosquée de Pau",
                "payment_instructions": "Veuillez taper ou insérer votre carte de crédit/débit ci-dessous"
            },
            "en": {
                "title": "I support the Mosque of Pau",
                "splash_title": "Payment Terminal",
                "splash_instruction": "Tap anywhere to continue",
                "adherents": "Members Area",
                "adherents_help": "Recharge your membership card",
                "coming_soon": "Coming soon",
                "mosque": "Donations for the mosque project",
                "mosque_help": "Help the mosque build a parking lot",
                "works": "Mosque Renovation",
                "works_help": "Support renovations and projects",
                "ramadan_title": "Donations for Ramadan",
                "sadaqa_button": "Donate for Iftar",
                "ramadan": "Ramadan",
                "ramadan_help": "Donations for Iftar and Zakât al-Fitr",
                "footer": "Edited by @adelhanifi",
                "language_label": "Language:",
                "other_amount": "Other\namount",
                "other_amount_title": "Enter an amount",
                "hide_amount": "Hide Amount",
                "show_amount": "Show Amount",
                "validate": "Validate",
                "invalid_amount": "Please enter a valid amount.",
                "back": "Back",
                "zakat": "pay 7€",
                "zakat_title": "Zakat al-Fitr",
                "zakat_explanation": "Zakat al-Fitr is set at €7 per person.\nPlease press the button below to pay it.",
                "zakat_button": "Pay Zakat al-Fitr (7 €)",
                "payment_title": "I SUPPORT",
                "payment_subtitle": "Mosque of Pau",
                "payment_instructions": "Please tap or insert your credit/debit card below"
            },
            "ar": {
                "title": "أدعم مسجد بو",
                "splash_title": "محطة الدفع",
                "splash_instruction": "انقر في أي مكان للمتابعة",
                "adherents": "فضاء الأعضاء",
                "adherents_help": "أعد شحن بطاقة العضو الخاصة بك",
                "coming_soon": "قريباً متوفر",
                "mosque": "التبرعات لمشروع المسجد ",
                "mosque_help": "ساعد المسجد في بناء موقف للسيارات",
                "works": "أعمال المسجد",
                "works_help": "دعم التجديدات والمشاريع",
                "ramadan": "رمضان",
                "ramadan_help": "تبرعات للإفطار وزكاة الفطر",
                "ramadan_title": "تبرعات لرمضان",
                "sadaqa_button": "تبرع للإفطار",
                "footer": "من إعداد @adelhanifi",
                "language_label": "اللغة:",
                "other_amount": "مبلغ آخر",
                "other_amount_title": "أدخل مبلغًا",
                "hide_amount": "إخفاء المبلغ",
                "show_amount": "إظهار المبلغ",
                "validate": "تأكيد",
                "invalid_amount": "يرجى إدخال مبلغ صالح.",
                "back": "عودة",
                "zakat_title": "زكاة الفطر",
                "zakat_explanation": "زكاة الفطر محددة بـ 7 يورو لكل شخص.\nيرجى الضغط على الزر أدناه للدفع.",
                "zakat": "ادفع 7 يورو",
                "zakat_button": "ادفع 7 يورو",
                "payment_title": "أدعم",
                "payment_subtitle": "مسجد بو",
                "payment_instructions": "يرجى النقر أو إدخال بطاقة الائتمان/الخصم الخاصة بك أدناه"
            },
        }


    def apply_styles(self):
        """
        Charge le fichier de styles QSS.
        """
        try:
            with open("templates/styles.qss", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Le fichier styles.qss est introuvable. Veuillez vérifier son emplacement.")

    def setup_ui(self):
        # Création du widget principal
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Barre de sélection de langue
        language_layout = QHBoxLayout()
        language_layout.addStretch()

        language_label = QLabel(self.translations[self.current_language]["language_label"])
        language_label.setFont(QFont("Arial", 12))
        language_layout.addWidget(language_label)

        self.language_selector = QComboBox()
        self.language_selector.addItems(["Français", "English", "العربية"])
        self.language_selector.currentIndexChanged.connect(self.change_language)
        language_layout.addWidget(self.language_selector)

        language_layout.addStretch()
        layout.addLayout(language_layout)

        
        logo = QLabel()
        logo_pixmap = QPixmap(":/images/mosquee_logo.png")

        # Vérifier si l'image a bien été chargée
        if logo_pixmap.isNull():
            print("Erreur : Impossible de charger l'image 'mosquee_logo.png'")
        else:
            logo_pixmap = logo_pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(logo_pixmap)
            logo.setAlignment(Qt.AlignCenter)


        # Titre sous le logo
        self.title = QLabel(self.translations[self.current_language]["title"])
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 60, QFont.Bold))

        # Boutons
        buttons_layout = QHBoxLayout()

        buttons = [
            {"key": "adherents", "help_key": "adherents_help", "icon": ":/images/adherents_icon.png", "handler": None},
            {"key": "mosque", "help_key": "mosque_help", "icon": ":/images/mosquee_icon.png", "handler": self.handle_mosque},
            {"key": "works", "help_key": "works_help", "icon": ":/images/travaux_icon.png", "handler": self.handle_works},
            {"key": "ramadan", "help_key": "ramadan_help", "icon": ":/images/ramadan_icon.png", "handler": self.handle_ramadan},
        ]

        self.buttons = []
        for button_data in buttons:
            # Conteneur vertical pour l'icône, le texte principal et l'aide
            button_layout = QVBoxLayout()
            buttons_layout.setSpacing(10)  # Espacement horizontal entre les boutons
            buttons_layout.setContentsMargins(50, 0, 50, 0)  # Marges autour du layout des boutons
            # Icône
            icon_label = QLabel()
            icon_pixmap = QPixmap(button_data["icon"]).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
            icon_label.setAlignment(Qt.AlignCenter)

            # Texte principal
            text_label = QLabel(self.translations[self.current_language][button_data["key"]])
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setFont(QFont("Arial", 27, QFont.Bold))

            # Texte d'aide
            help_label = QLabel(self.translations[self.current_language][button_data["help_key"]])
            help_label.setAlignment(Qt.AlignCenter)
            help_label.setFont(QFont("Arial", 14))
            help_label.setStyleSheet("color: gray;")

            # Ajouter les éléments au layout
            button_layout.addWidget(icon_label)
            button_layout.addWidget(text_label)
            button_layout.addWidget(help_label)

            # Encapsuler dans un bouton
            button_container = QPushButton()
            button_container.setLayout(button_layout)
            button_container.setMinimumSize(200, 200)
            button_container.setObjectName("homeButton")  # Appliquer le style spécifique

            # Connecter le gestionnaire de clic, si défini
            if button_data["handler"]:
                button_container.clicked.connect(button_data["handler"])

            # Ajouter le bouton au layout horizontal
            buttons_layout.addWidget(button_container)
            self.buttons.append((text_label, help_label, button_data["key"], button_data["help_key"]))

        # Ajouter les widgets au layout principal
        layout.addWidget(logo)  # Logo
        layout.addWidget(self.title)  # Titre
        layout.addLayout(buttons_layout)  # Boutons
        layout.addStretch()  # Espacement

        # Texte en bas de l'écran
        self.footer = QLabel(self.translations[self.current_language]["footer"])
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setFont(QFont("Arial", 10))
        layout.addWidget(self.footer)

        # Appliquer le layout principal
        main_widget.setLayout(layout)
        return main_widget

    def handle_mosque(self):
        """
        Gère la redirection vers la page des dons.
        """
        self.pages.setCurrentWidget(self.dons_page)
    def handle_ramadan(self):
        """
        Navigue vers la page de Ramadan.
        """
        self.pages.setCurrentWidget(self.ramadan_page)

    def handle_works(self):
        self.pages.setCurrentWidget(self.works_page)
    def update_translations(self, translations, current_language):
        """Met à jour les textes de la page d'accueil avec la nouvelle langue."""
        self.translations = translations
        self.current_language = current_language

        print(f" Mise à jour HomePage avec {current_language}")

        # Vérifier que les labels existent avant de les modifier
        if hasattr(self, "title") and isinstance(self.title, QLabel):
            self.title.setText(self.translations[current_language].get("title", "Titre par défaut"))
            print(f" Mise à jour du titre : {self.title.text()}")
        if hasattr(self, "footer") and isinstance(self.footer, QLabel):
            self.footer.setText(self.translations[current_language].get("footer", ""))
            print(f" Mise à jour du footer : {self.footer.text()}")

        for text_label, help_label, key, help_key in self.buttons:
            if isinstance(text_label, QLabel):
                text_label.setText(self.translations[current_language].get(key, ""))
                print(f" Mise à jour du texte : {text_label.text()}")
            if isinstance(help_label, QLabel):
                help_label.setText(self.translations[current_language].get(help_key, ""))
                print(f" Mise à jour de l'aide : {help_label.text()}")

        print("✅ Mise à jour terminée pour HomePage")


    def change_language(self, new_language):
        """Met à jour la langue et applique la traduction à toutes les pages."""

        # 🔴 Vérification que `new_language` est une chaîne et non un index
        if not isinstance(new_language, str):
            print(f" Erreur : Langue reçue non valide ({new_language})")
            return

        # 🔴 Vérifier que la langue existe dans `translations`
        if new_language not in self.translations:
            print(f" Erreur : Langue inconnue {new_language}")
            return

        self.current_language = new_language
        print(f" Changement de langue appliqué : {self.current_language}")

        # 🔴 Appliquer la nouvelle langue à toutes les pages
        for page in [self.splash_page, self.home_page, self.dons_page, self.ramadan_page, 
                    self.iftar_page, self.zakat_page, self.works_page, self.otheramount_page, 
                    self.payment_page]:
            if hasattr(page, 'update_translations'):
                print(f" Mise à jour de {page.__class__.__name__}")
                page.update_translations(self.translations, self.current_language)



        for text_label, help_label, key, help_key in self.buttons:
            text_label.setText(self.translations[self.current_language].get(key, ""))
            help_label.setText(self.translations[self.current_language].get(help_key, ""))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainApp()
    window.show()
    sys.exit(app.exec())
'''
if __name__ == "__main__":
    api_key = "sup_sk_YkWjlUS5edcb0LAVsObRwsJXJu9dMyH6o"  # Remplacez par votre clé API
    merchant_code = "MFT77XNQ"  # Remplacez par votre code marchand
    pairing_code = "EZRVUID3R"  # Remplacez par le code de pairing affiché sur le terminal

    sumup = SumUpIntegration(api_key, merchant_code)
    terminal_details = sumup.pair_terminal(pairing_code)

    if terminal_details:
        print("Terminal pairé avec succès :", terminal_details)
    else:
        print("Le pairing du terminal a échoué.")
'''