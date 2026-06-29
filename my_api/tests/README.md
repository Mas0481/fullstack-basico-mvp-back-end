# \# Como executar o projeto

# 

# \## Pré-requisitos

# 

### Antes de iniciar, certifique-se de ter instalado:

### 

### \- Python 3.11 ou superior

### \- Git

### \- Visual Studio Code (recomendado)

### \- Extensão \*\*Python\*\* para o VS Code

### 

### \---

# 

# \## 1. Clonar o repositório

# 

### ```bash

### git clone <URL\_DO\_REPOSITORIO>

### cd <NOME\_DO\_REPOSITORIO>

### ```

### ou copiar manualmente o código do repositório do git

### \---

# 

# \## 2. Criar o ambiente virtual

# 

### \### Windows (PowerShell ou CMD)

### 

### ```bash

### python -m venv .venv

### ```

### 

### \### Linux / macOS

### 

### ```bash

### python3 -m venv .venv

### ```

### 

### \---

### 

### \## 3. Ativar o ambiente virtual

### 

### \### Windows (PowerShell)

### 

### ```powershell

### .\\.venv\\Scripts\\Activate.ps1

### ```

### 

### > Caso seja exibido um erro relacionado à política de execução, execute:

### 

### ```powershell

### Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

### ```

### 

### Depois execute novamente:

### 

### ```powershell

### .\\.venv\\Scripts\\Activate.ps1

### ```

### 

### \### Windows (Prompt de Comando - CMD)

### 

### ```cmd

### .\\.venv\\Scripts\\activate.bat

### ```

### 

### \### Linux / macOS

### 

### ```bash

### source .venv/bin/activate

### ```

### 

### Quando o ambiente estiver ativo, o terminal exibirá algo semelhante a:

### 

### ```text

### (.venv)

### ```

### 

### \---

### 

# \## 4. Instalar as dependências

### 

### ```bash

### pip install -r requirements.txt

### ```

### 

### \---

# 

# \## 5. Configurar o Visual Studio Code

# 

### Abra o projeto no VS Code.

### 

### Caso o interpretador Python não seja selecionado automaticamente:

### 

### 1\. Pressione \*\*Ctrl + Shift + P\*\*

### 2\. Digite:

### 

### ```

### Python: Select Interpreter

### ```

### 

### 3\. Selecione o interpretador localizado em:

### 

### \*\*Windows\*\*

### 

### ```

### .venv\\Scripts\\python.exe

### ```

### 

### \*\*Linux/macOS\*\*

### 

### ```

### .venv/bin/python

### ```

### 

### \---

# 

# \## 6. Executar a aplicação

# 

### ```bash

### python -m flask --app my\_api.main run --reload

### ```

### 

### A aplicação estará disponível em:

### 

### ```

### http://127.0.0.1:5000

### ```

### 

### \---

# 

# \## 7. Documentação da API

# 

### Após iniciar a aplicação, a documentação interativa da API poderá ser acessada em:

### 

### ```

### http://127.0.0.1:5000/docs

### ```

### 

### \---



# \## 8. Resposta padronizada da API

# 

### Sucesso:

### 

### ```json

### {

### &#x20; "status": "sucesso",

### &#x20; "mensagem": "...",

### &#x20; "data": {}

### }

### ```

### 

### Erro:

### 

### ```json

### {

### &#x20; "status": "erro",

### &#x20; "mensagem": "...",

### &#x20; "detalhes": \[]

### }

### ```

# 

# \## Encerrar o ambiente virtual

# 

### Quando terminar o desenvolvimento:

### 

### ```bash

### deactivate

### ```

