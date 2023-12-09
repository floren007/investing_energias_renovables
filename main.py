# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import pandas as pd
from selenium.webdriver.support.ui import Select
# %%
# The sleep function can help you to avoid the server 
# to be overloaded with too many requests in a very short period of time. Basically, with sleep you can make the script stop for a certain period of time so that if you are making some requests iteratively you can avoid the server to be overloaded.
def sleep():
    time.sleep(random.randint(1,3))
# %%
# create a conection with the driver google
driver = webdriver.Chrome(ChromeDriverManager().install())
ingesta = {"Invesco Solar ETF (TAN)": "https://es.investing.com/etfs/claymore-mac-global-solar-energy-in",
           "Lyxor Green Bond DR UCITS C-EUR (CLIM)": "https://es.investing.com/etfs/lyxor-green-bond-dr-c-eur",
           "iShares Global Clean Energy ETF (ICLN)": "https://es.investing.com/etfs/ishares-s-p-global-clean-energy",
           "SPDR® Kensho Clean Power ETF (CNRG)": "https://es.investing.com/etfs/cnrg",
           "NASDAQ Clean Edge Green Energy (CELS)": "https://es.investing.com/indices/nasdaq-clean-edge-green-energy"}
# %%
driver.get("https://es.investing.com/")
sleep()
boton = driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
# %%
dataframe1 = pd.DataFrame(data=None)
data = {}
dataframeBusines = pd.DataFrame(data=None)
elements = driver.find_elements(By.CLASS_NAME, 'flex-1')
for name,url in ingesta.items():
    driver.get(url)
    driver.refresh()
    print(name + " -> "+ url)
    sleep()
    find_name = driver.find_elements(By.TAG_NAME,'dt')
    find_value = driver.find_elements(By.TAG_NAME,'dd')
    for campo,valor in zip(find_name,find_value):
        campo = campo.text
        valor = valor.text
        data["Nombre"] = name
        data[campo] = valor
    datos = pd.DataFrame([data])
    dataframe1 = pd.concat([dataframe1,datos])
    informacionHistorica = driver.find_element(By.XPATH, "//a[contains(text(), 'Información histórica')]")
    driver.execute_script("arguments[0].click();",informacionHistorica)
    sleep()
    driver.find_element(By.CLASS_NAME,'historical-data-v2_selection-arrow__3mX7U').click()
    driver.find_element(By.XPATH, "//span[contains(text(), 'Mensual')]").click()
    sleep()
    tablilla = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/table').get_attribute('outerHTML')
    df = pd.read_html(tablilla)[0]
    df["Nombre"] = (name) * len(df)
    dataframeBusines = pd.concat([dataframeBusines,df])
    driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/nav/div[1]/ul/li[4]').click()
    driver.find_element(By.XPATH, "//span[contains(text(), 'Mensual')]").click()
    ind_tecnico = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[4]/div/div[2]/div[2]/div[2]/div/table').get_attribute('outerHTML')
    df_ind_tecnico_tabla_mensual = pd.read_html(ind_tecnico)[0]
    df_ind_tecnico_tabla_mensual["Nombre_emp"] = (name) * len(df)
    dataframe_ind_tecnico = pd.concat([dataframe_ind_tecnico,df_ind_tecnico_tabla_mensual])
print(dataframe1)
# %%
