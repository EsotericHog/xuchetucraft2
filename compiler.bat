pyinstaller --noconfirm --onedir --windowed --hidden-import=dotenv --noconsole ^
--icon="assets\panda.ico" ^
--add-data "assets\panda.ico;assets" ^
--add-data "assets\Bannerv2.jpg;assets" ^
--add-data "assets\fabric_logo.png;assets" ^
--add-data "assets\novaskin-wallpaper-llama_cutv2.jpg;assets" ^
--add-data "assets\xc2_bg.jpg;assets" ^
--add-data "auth\google_cloud_credentials.json;auth" ^
--add-data ".env;." ^
--add-data ".venv\Lib\site-packages\customtkinter;customtkinter" ^
--name="Xuchetucraft2" ^
"main.py"