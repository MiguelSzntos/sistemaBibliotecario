# Fase 1 - Configuração Inicial e Conexão com o Banco de Dados
# Objetivos: Importar bibliotecas e criar Conexão com MySQL

# Importa a biblioteca CustomTkinter para criar interfaces modernas
import customtkinter as ctk

# Importa módulos auxiliares do Tkinter para mensagens e tabelas
from tkinter import messagebox, ttk

# Importa módulo para a conexão ao MySQL
import mysql.connector

# Importa módulos para trabalhar com datas
from datetime import date, timedelta

# Importa módulos para gerar números aleatórios 
import random

# ------- CONEXÃO COM MYSQL -------
# Função para criar a conexão com o banco de dados
def conectar():
    return mysql.connector.connect(
        host="localhost", # Endereço do servidor do banco (localhost = Este computador)
        user="root", # Usuário do banco
        password="", # Senha do banco
        database="biblioteca2" # Nome do banco de dados
    )

# ------------------------------------------------------------ #

# Fase 2 - Gerador ID's Únicos
# Objetivos: Gerar identificadores únicos e verificar duplicidade no banco

# ------- GERADOR DE IDS ALEATÓRIOS ÚNICOS -------

def gerar_id_unico(tabela, coluna):
    # Define os prefixos para cada tipo de tabela
    prefixos = {
        "Cliente":"C",
        "Livro":"L",
        "Emprestimos":"E",
        "Categoria":"CA",
        "Usuarios":"U"
    }

    # Pega o prefixo correspondente à tabela, ou vazio se não definido
    prefixo = prefixos.get(tabela,"")

    conn = conectar() # Conecta ao banco
    cursor = conn.cursor() # Cria cursor para executar comando SQL
    while True:
        numero = random.randint(1000, 9999) # Gera número aleatório
        novo_id = f"{prefixo}{numero}" # Junta prefixo + número

        # Verifica se o ID já existe na tabela
        cursor.execute(f"SELECT {coluna} FROM {tabela} WHERE {coluna}=%s", (novo_id,))
        if not cursor .fetchone():
            conn.close()
            return novo_id
        
# ------------------------------------------------------------ #

# Fase 3 - Configuração da Janela Principal
# Objetivos: Criação da janela principal e inicialização da aplicação desktop

# Define o tema escuro e cor padrão do app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Classe principal do aplicativo
class Biblioteca(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Biblioteca") # Título da janela
        self.geometry("1000x650") # Tamanho da janela
        self.minsize(750, 600) # Coloca um tamanho mínimo para a janela
        self.maxsize(1000, 650) # Coloca um tamanho máximo para a janela
        self.resizable(True, True) # Bloqueia redimensionamento
        self.frame_login() # Mostra tela de login inicialmente
        self.btn_status = None # Inicializa atributo para botões de Status

# ------------------------------------------------------------ #

# Fase 4 - Tela de Login
# Objetivos: Entrada de dados, botões e verificação básica de Login

    # Método que cria o frame de Login
    def frame_login(self):
        self.clear_screen() # Limpa tela antes de mostrar Login
        frame = ctk.CTkFrame(self, width=300, height=300, fg_color="grey") # Cria a tela do Login
        frame.pack(expand=True) # Centraliza a tela do Login
        frame.propagate(False) # Impede que o frame redimensione de acordo com os Widgets

        lbl_title = ctk.CTkLabel(frame, text="Login Sistema", font=("Arial", 20))
        lbl_title.pack(pady=20)

        # Entrada de usuário
        self.text = ctk.CTkLabel(frame, text="Usuário", text_color="White", font=("Arial", 15))
        self.text.pack(anchor="w", padx=86)
        # Texto acima da caixa
        self.entry_user = ctk.CTkEntry(frame, placeholder_text="Usuário", fg_color="black")
        self.entry_user.pack(pady=(0,10))
        
        self.text = ctk.CTkLabel(frame, text="Senha", text_color="White", font=("Arial", 15))
        self.text.pack(anchor="w", padx=86)

        # Entrada de senha
        self.entry_pass = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", fg_color="black")
        self.entry_pass.pack(pady=(0,10))

        # Botão para tentar Login
        btn_login = ctk.CTkButton(frame, text="Entrar", command=self.login)
        btn_login.pack(pady=20)

        # Botão para criar Conta
        btn_criar_contar = ctk.CTkButton(frame, text="Criar Conta", fg_color="Purple" ,hover_color="dark violet", command=self.criar_conta)
        btn_criar_contar.pack(pady=5)

    def login(self):
        # Define e relaciona as funções de User e Password
        user = self.entry_user.get()
        password = self.entry_pass.get()
        if user == "admin" and password == "123":
            self.frame_main()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def criar_conta(self):
        # Cria uma nova janela (Janela filha) sobre a principal
        win = ctk.CTkToplevel(self)
        win.title("Criação de Conta")
        win.geometry("350x300")

        # Faz com que a janela fique em foco principal
        win.attributes("-topmost", True)

        # Cria um campo de texto para digitar o Nome do Usuário
        nome_usuario = ctk.CTkEntry(win, placeholder_text="Nome")
        nome_usuario.pack(pady=5)

        # Cria um campo de texto para digitar a Senha do Usuário
        senha_u = ctk.CTkEntry(win, placeholder_text="Senha")
        senha_u.pack(pady=5)

        # Cria um campo de texto para digitar o CPF do Usuário
        cpf_usuario = ctk.CTkEntry(win, placeholder_text="CPF")
        cpf_usuario.pack(pady=5)

        # Cria um campo de texto para digitar o telefone do cliente
        email = ctk.CTkEntry(win, placeholder_text="E-mail")
        email.pack(pady=5)

        btn_cadastrar = ctk.CTkButton(win, text="Cadastrar", command=self.salvar_usuario_cliente)
        btn_cadastrar.pack(pady=20)

    def salvar_usuario_cliente(self, nome_usuario, senha_u, cpf_usuario, email, win):
        if not nome_usuario or not cpf_usuario:
            messagebox.showwarning("Aviso", "Nome de Usuário e CPF são obrigátorios.")
            return
        id_usuario = gerar_id_unico("Usuarios", "id_usuario")
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (id_usuario, nome_usuario, senha, cpf)")
        

# ------------------------------------------------------------ #

# Fase 5 - Tela Principal e Menu Lateral
# Objetivos: Criação de Layout com Menu Lateral e Área de Conteúdo
    def frame_main(self):

        self.clear_screen() # Limpa a tela

        # Menu lateral com Botões
        menu_frame = ctk.CTkFrame(self, width=200)
        menu_frame.pack(side="left", fill="y")

        # Botões do menu
        btn_home = ctk.CTkButton(menu_frame, text="Resumo", command=self.frame_resumo)
        btn_home.pack(pady=10)

        btn_cliente = ctk.CTkButton(menu_frame, text="Cadastro Cliente", command=self.frame_cliente)
        btn_cliente.pack(pady=10)

        btn_livros = ctk.CTkButton(menu_frame, text="Cadastro Livro", command=self.frame_livro)
        btn_livros.pack(pady=10)

        btn_emprestimo = ctk.CTkButton(menu_frame, text="Gerenciar Empréstimos", command=self.frame_emprestimo)
        btn_emprestimo.pack(pady=10)

        btn_sair = ctk.CTkButton(menu_frame, text="Sair", command=self.frame_login)
        btn_sair.pack(pady=10)

        # Área principal que muda conforme o frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", expand=True, fill="both")

        self.frame_resumo()

# ------------------------------------------------------------ #

# Fase 6 - Cadastro de Cliente (CRUD Básico)
# Objetivos:
# Mostrar Treeview para listar clientes
# Inserir, editar e alternar status.

    def frame_cliente(self):
        self.clear_main() # Limpa a área principal
        lbl = ctk.CTkLabel(self.main_frame, text="Gerenciador de Clientes", font=("Arial", 18))
        lbl.pack(pady=20)

        # Treeview para mostrar clientes
        self.tree_cliente = ttk.Treeview(self.main_frame, columns=("ID", "Nome", "CPF", "Data Nascimento", "Telefone", "Status"), show="headings", height=10)
        for coluna in ("ID", "Nome", "CPF", "Data Nascimento", "Telefone", "Status"):
            self.tree_cliente.heading(coluna, text=coluna)

        self.tree_cliente.pack(pady=10, fill="x") # Importante: Mostra a Tabela

        self.carregar_cliente() # Carrega clientes do banco

        # Botões de ação
        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir_cliente).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Editar", command=self.editar_cliente).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Deletar", command=self.deletar_cliente).pack(side="left", padx=5)

        self.btn_status = ctk.CTkButton(
            btn_frame,
            text="Desativar",
            command=lambda: self.alternar_status(
                self.tree_cliente,     # Treeview
                "Cliente",             # Nome da tabela
                "id_cliente",          # Coluna ID
                "status",              # Coluna de status
        self.carregar_cliente, # Função para recarregar os dados
        self.atualizar_botao_status  # Atualiza o botão após alterar
            )
        )

        self.btn_status.pack(side="left", padx=5)

        # Atualiza o texto do botão ao selecionar outro cliente
        self.tree_cliente.bind("<<TreeviewSelect>>", lambda e: self.atualizar_botao_status(self.tree_cliente, self.btn_status))

    def carregar_cliente(self):

        # Percorre todos os itens que já estão no Treeview (A tabela da interface)
        for row in self.tree_cliente.get_children():
            
            # Remove cada item, garantindo que a tabela seja limpa antes de recarregar os dados
            self.tree_cliente.delete(row)
            
        conn = conectar() # Abre uma conexão com o banco de dados usando a função 'conectar()'

        cursor = conn.cursor() # Cria um cursor, que é o objeto responsável por executar comandos SQL

        # Executa um comando SQL para buscar todos os clientes no banco
        cursor.execute("SELECT id_cliente, nome_cliente, cpf, data_nascimento, telefone, status FROM Cliente")

        # Percorre todos os resultados retornados para consulta SQL
        for row in cursor.fetchall():

            # Insere cada linha de dados dentro do Treeview da interface gráfica
            # O Parâmetro values=row coloca os valores retornados na tabela
            self.tree_cliente.insert("", "end", values=row)
            conn.close()

    def inserir_cliente(self):

        # Cria uma nova janela (Janela filha) sobre a principal
        win = ctk.CTkToplevel(self)
        win.title("Novo cliente")
        win.geometry("350x300")

        # Mantém essa janela sempre na frente, até ser fechada
        win.attributes("-topmost", True)

        # Cria um campo de texto para digitar o nome do cliente
        nome = ctk.CTkEntry(win, placeholder_text="Nome")
        nome.pack(pady=5)

        # Cria um campo de texto para digitar o CPF do cliente
        cpf = ctk.CTkEntry(win, placeholder_text="CPF")
        cpf.pack(pady=5)

        data_nascimento = ctk.CTkEntry(win, placeholder_text="AAAA-MM-DD")
        data_nascimento.pack(pady=5)

        # Cria um campo de texto para digitar o telefone do cliente
        telefone = ctk.CTkEntry(win, placeholder_text="Telefone")
        telefone.pack(pady=5)

        # Cria um rótulo (texto fixo) indicando o campo de Status
        lbl_status = ctk.CTkLabel(win, text="Status")
        lbl_status.pack(pady=5)
        
        # Cria uma caixa de seleção com duas opções: "Ativo" e "Inativo"
        cb_status = ctk.CTkComboBox(win, values=["Ativo", "Inativo"])
        cb_status.set("Ativo") # Define "Ativo" como valor padrão
        cb_status.pack(pady=5)

        # Cria um botão "Salvar" quando clicado, chama a função salvar_cliente_janela
        btn = ctk.CTkButton(win, text="Salvar", command=lambda: self.salvar_cliente_janela (nome.get(), cpf.get(), data_nascimento.get(), telefone.get(), cb_status.get(), win))
        btn.pack(pady=10)

    def salvar_cliente_janela(self, nome_cliente, cpf, data_nascimento, telefone, status, win):
        if not nome_cliente or not cpf:
            messagebox.showwarning("Aviso", "Nome e CPF são obrigatórios.")
            return
        id_cliente = gerar_id_unico("Cliente", "id_cliente")
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Cliente (id_cliente, nome_cliente, cpf, data_nascimento, telefone, status) VALUES (%s,%s,%s,%s,%s,%s)", (id_cliente, nome_cliente, cpf, data_nascimento, telefone, status))

        conn.commit()
        conn.close()
        self.carregar_cliente()
        win.destroy()
        messagebox.showinfo("Sucesso", f"Cliente cadastrado com ID{id_cliente}!")

    def editar_cliente(self):
        item = self.tree_cliente.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar.")
            return
        id_cliente, nome, cpf, data_nascimento, telefone, status = self.tree_cliente.item(item, "values")
        win = ctk.CTkToplevel(self)
        win.title("Editar Cliente")
        win.geometry("350x300")
        win.attributes("-topmost", True)

        nome_e = ctk.CTkEntry(win)
        nome_e.insert(0, nome)
        nome_e.pack(pady=5)

        cpf_e = ctk.CTkEntry(win)
        cpf_e.insert(0, cpf)
        cpf_e.pack(pady=5)

        data_nas_e = ctk.CTkEntry(win)
        data_nas_e.insert(0, data_nascimento)
        data_nas_e.pack(pady=5)

        tel_e = ctk.CTkEntry(win)
        tel_e.insert(0, telefone)
        tel_e.pack(pady=5)

        lbl_status = ctk.CTkLabel(win, text="Status:")
        lbl_status.pack(pady=5)

        cb_status = ctk.CTkComboBox(win, values=["Ativo", "Inativo"])
        cb_status.set(status)
        cb_status.pack(pady=5)

        btn = ctk.CTkButton(win, text="Salvar", command=lambda: self.salvar_edicao_cliente(id_cliente, nome_e.get(), cpf_e.get(), data_nas_e.get(), tel_e.get(), cb_status.get(), win))
        btn.pack(pady=10)

    def salvar_edicao_cliente(self, id_cliente, nome, cpf, data_nascimento, telefone, status, win):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE Cliente SET nome_cliente=%s, cpf=%s, data_nascimento=%s, telefone=%s, status=%s WHERE id_cliente=%s", (nome, cpf, data_nascimento, telefone, status, id_cliente))
        conn.commit()
        conn.close()
        self.carregar_cliente()
        win.destroy()
        messagebox.showinfo("Sucesso", "Cliente atualizado.")

    # Função genérica para alternar status (Cliente, Livro, Empréstimo)

    def alternar_status(self, tree, tabela, id_coluna, status_coluna, carregar_func, atualizar_func=None, status_ativo="Ativo", status_inativo="Inativo"):

        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um registro para alterar o status")
            return

        valores = tree.item(item, "values")
        id_registro = valores[0]
        status_atual = valores[-1]

        # Alterna status
        novo_status = status_inativo if status_atual == status_ativo else status_ativo
        
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE {tabela} SET {status_coluna}=%s WHERE {id_coluna}=%s", (novo_status, id_registro)
            )
            conn.commit()
            conn.close()

            carregar_func() # Atualiza a tabela
            if atualizar_func:
                atualizar_func()
            messagebox.showinfo("Sucesso", f"Status alterado para {novo_status}.")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar o status. \n\n{e}")
    

    def atualizar_botao_status(self, tree=None, btn_status=None):
        if tree is None or btn_status is None:
            return # Se não recever tabela ou botão, não faz nada
        
        selecionado = tree.selection()
        if not selecionado:
            btn_status.configure(text="Desativar")
            return
         
        status = tree.item(selecionado[0], "values")[-1].strip().lower()
        btn_status.configure(text="Desativar" if status == "ativo" else "Ativar")

    def deletar_cliente(self):
        item = self.tree_cliente.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro para Deletar")
            return
        cliente_id = self.tree_cliente.item(item, "values") [0]
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Emprestimos WHERE id_cliente=%s", (cliente_id,))
        count = cursor.fetchone() [0]
        if count > 0:
            messagebox.showwarning("Aviso", "ID já vinculado, recomendo desativar primeiro antes da Exclusão.")
            conn.close()
            return
        else:
            cursor.execute("DELETE FROM Cliente WHERE id_cliente=%s", (cliente_id))
        conn.commit()
        conn.close()
        self.carregar_livros()
        messagebox.showinfo("Sucesso", "Cliente deletado com sucesso")

    
    # ============================== CADASTRO LIVRO ==============================
    def frame_livro(self):
        self.clear_main()
        lbl = ctk.CTkLabel(self.main_frame, text="Gerenciador de Livros", font=("Arial", 18))
        lbl.pack(pady=20)

        # Treeview para Livros
        self.tree_livro = ttk.Treeview(self.main_frame, columns=("ID", "Título", "Autor", "Ano", "Gênero", "Status"), show="headings", height=10)
        self.tree_livro.pack(pady=10, padx=1, fill="both")

        for col in ("ID", "Título", "Autor", "Ano", "Gênero", "Status"):
            self.tree_livro.heading(col, text=col)
        self.carregar_livros()

        # Botões de ação
        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir_livro).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Editar", command=self.editar_livro).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Deletar", command=self.deletar_livro).pack(side="left", padx=5)

        self.btn_status = ctk.CTkButton(
        btn_frame,
        text="Desativar",
        command=lambda: self.alternar_status(
        self.tree_livro,
            "Livro",
            "id_livro",
            "status",
        self.carregar_livros,
        )
    )
        self.tree_livro.bind("<<TreeviewSelect>>", lambda e: self.atualizar_botao_status(self.tree_livro, self.btn_status))
        self.btn_status.pack(side="left", padx=5)

    def carregar_livros(self):

        # Percorre todos os itens que já estão no Treeview (A Tabela da Interface)
        for row in self.tree_livro.get_children():

            # Remove cada item, garantindo que a tabela seja limpa antes de recarregar os dados
            self.tree_livro.delete(row)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_livro, titulo_livro, autor_livro, ano, genero, status FROM Livro")
        for row in cursor.fetchall():
            self.tree_livro.insert("", "end", values=row)
        conn.close()

    def inserir_livro(self):
        win = ctk.CTkToplevel(self)
        win.title("Novo Livro")
        win.geometry("350x300")
        
        # Mantém essa janela sempre na frente, até ser fechada
        win.attributes("-topmost", True)

        # Cria um campo de texto para digitar o nome do Livro
        titulo_livro = ctk.CTkEntry(win, placeholder_text="Título")
        titulo_livro.pack(pady=5)

        # Cria um campo de texto para digitar o nome do Autor
        autor_livro = ctk.CTkEntry(win, placeholder_text="Autor")
        autor_livro.pack(pady=5)

        # Cria um campo de texto para digitar o ano
        ano = ctk.CTkEntry(win, placeholder_text="Ano")
        ano.pack(pady=5)

        # Cria um rótulo (texto fixo) indicando o campo de gênero
        genero = ctk.CTkEntry(win, placeholder_text="Gênero")
        genero.pack(pady=5)

        # Cria um rótulo (texto fixo) indicando o campo de Status
        lbl_status = ctk.CTkLabel(win, text="Status")
        lbl_status.pack(pady=5)
        
        # Cria uma caixa de seleção com duas opções: "Ativo" e "Inativo"
        cb_status = ctk.CTkComboBox(win, values=["Ativo", "Inativo"])
        cb_status.set("Ativo") # Define "Ativo" como valor padrão
        cb_status.pack(pady=5)

        btn = ctk.CTkButton(win, text="Salvar", command=lambda: self.salvar_livro_janela(titulo_livro.get(), autor_livro.get(), ano.get(), genero.get(), cb_status.get(), win))
        btn.pack(pady=5)

    def salvar_livro_janela(self, titulo_livro, autor_livro, ano, genero, status, win, id_livro=None):
        if not titulo_livro or not autor_livro:
            messagebox.showwarning("Aviso, Título e Autor são obrigatórios")
            return
        
        conn = conectar()
        cursor = conn.cursor()

        if not id_livro:
            # Inserção: Gera novo ID
            id_livro = gerar_id_unico("Livro", "id_livro")
            cursor.execute(
                "INSERT INTO Livro (id_livro, titulo_livro, autor_livro, ano, genero, status) VALUES (%s,%s,%s,%s,%s,%s)",
                (id_livro, titulo_livro, autor_livro, ano, genero, status)
            )
            msg = f"Livro cadastrado com ID: {id_livro}"
        else:
            # Edição: Usa ID Existente
            cursor.execute(
                "UPDATE Livro SET titulo_livro=%s, autor_livro=%s, ano=%s, genero=%s, status=%s WHERE id_livro=%s",
                (titulo_livro, autor_livro, ano, genero, status, id_livro)
            )
            msg = "Livro atualizado com sucesso!"

        conn.commit()
        conn.close()
        self.carregar_livros()
        win.destroy()
        messagebox.showinfo("Sucesso", msg)
    
    def editar_livro(self):
        item = self.tree_livro.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro para editar")
            return
        
        # Pega os valoes do livro selecionado
        id_livro, titulo_livro, autor_livro, ano, genero, status = self.tree_livro.item(item, "values")

        win = ctk.CTkToplevel(self)
        win.title("Editar Livro")
        win.geometry("350x300")
        win.attributes("-topmost", True)

        titulo_e = ctk.CTkEntry(win)
        titulo_e.insert(0, titulo_livro)
        titulo_e.pack(pady=5)

        autor_e = ctk.CTkEntry(win)
        autor_e.insert(0, autor_livro)
        autor_e.pack(pady=5)

        ano_e = ctk.CTkEntry(win)
        ano_e.insert(0, ano)
        ano_e.pack(pady=5)

        genero_e = ctk.CTkEntry(win)
        genero_e.insert(0, genero)
        genero_e.pack(pady=5)

        lbl_status = ctk.CTkLabel(win, text="Status:")
        lbl_status.pack(pady=5)

        cb_status = ctk.CTkComboBox(win, values=["Ativo", "Inativo"])
        cb_status.set(status)
        cb_status.pack(pady=5)

        btn = ctk.CTkButton(win, text="Salvar", command=lambda: self.salvar_livro_janela(
                titulo_e.get(),
                autor_e.get(),
                ano_e.get(),
                genero_e.get(),
                cb_status.get(),
                win, id_livro))
        btn.pack(pady=10)

    def desativar_livro(self):
        item = self.tree_livro.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro para desativar")
            return
        livro_id = self.tree_livro.item(item, "values") [0]
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE Livro SET status='Inativo' WHERE id_livro=%s", (livro_id))
        conn.commit()
        conn.close()
        self.carregar_livros()
        messagebox.showinfo("Sucesso", "Livro desativado com sucesso")

    def deletar_livro(self):
        item = self.tree_livro.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um livro para Deletar")
            return
        livro_id = self.tree_livro.item(item, "values") [0]
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM emprestimos WHERE id_livro = %s", (livro_id,))
        count = cursor.fetchone() [0]
        if count > 0:
            messagebox.showwarning("Aviso", "ID já vinculado, recomendo desativar primeiro antes da Exclusão.")
            conn.close()
            return
        else:
            cursor.execute("DELETE FROM Livro WHERE id_livro=%s", (livro_id,))
        conn.commit()
        conn.close()
        self.carregar_livros()
        messagebox.showinfo("Sucesso", "Livro deletado com sucesso")

    # ============================== CADASTRO LIVRO ==============================

    def frame_emprestimo(self):
        self.clear_main()
        lbl = ctk.CTkLabel(self.main_frame, text="Gerenciar Empréstimos", font=("Arial", 18))
        lbl.pack(pady=20)

        self.tree_emp = ttk.Treeview(self.main_frame, columns=("ID_Empréstimo", "Cliente", "Livro", "Data_Empréstimo", "Data_Devolução"), show="headings", height=10)
        self.tree_emp.pack(pady=10, padx=10, fill="both")

        for col in ("ID_Empréstimo", "Cliente", "Livro", "Data_Empréstimo", "Data_Devolução"):
            self.tree_emp.heading(col, text=col)
        
        self.carregar_emprestimos()

        # Botões de ação
        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir_emprestimos).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Editar", command=self.editar_emprestimos).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Deletar", command=self.deletar_emprestimo).pack(side="left", padx=5)

    def carregar_emprestimos(self):
        for row in self.tree_emp.get_children():
            self.tree_emp.delete(row)
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
                SELECT
                e.id_emprestimo, 
                c.nome_cliente,
                l.titulo_livro,
                e.data_emprestimo,
                e.data_devolucao
                       
                FROM Emprestimos e
                JOIN Cliente c ON e.id_cliente = c.id_cliente
                JOIN Livro l ON e.id_livro = l.id_livro
        ''')

        for row in cursor.fetchall():
            self.tree_emp.insert("", "end", values=row)
        conn.close()

    def inserir_emprestimos(self):
        win = ctk.CTkToplevel(self)
        win.title("Novo Empréstimo")
        win.geometry("350x300")
        win.attributes("-topmost", True)

        lbl1 = ctk.CTkLabel(win, text="Cliente:")
        lbl1.pack(pady=5)
        clientes = self.get_clientes()
        cb_cliente = ctk.CTkComboBox(win, values=[f"{c[0]} - {c[1]}" for c in clientes])
        cb_cliente.pack(pady=5)

        lbl2 = ctk.CTkLabel(win, text="Livro:")
        lbl2.pack(pady=5)
        livros = self.get_livros()
        cb_livro = ctk.CTkComboBox(win, values=[f"{l[0]} - {l[1]}" for l in livros])
        cb_livro.pack(pady=5)

        btn = ctk.CTkButton(win, text="Salvar", command=lambda: self.salvar_emprestimo(cb_cliente.get(), cb_livro.get(), win))
        btn.pack(pady=20)

    def editar_emprestimos(self):
        item = self.tree_emp.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um empréstimo para editar.")
            return
        
        id_emp, nome_cliente, titulo_livro, data_emp, data_dev = self.tree_emp.item(item, "values")

        win = ctk.CTkToplevel(self)
        win.title("Editar Empréstimo")
        win.geometry("350x300")
        win.attributes("-topmost", True)

        lbl = ctk.CTkLabel(win, text=f"Edição devolução do Livro '{titulo_livro}'")
        lbl.pack(pady=10)

        entry_dev = ctk.CTkEntry(win, placeholder_text="Data Devolução (AAAA-MM-DD)")
        entry_dev.insert(0, data_dev if data_dev else "")
        entry_dev.pack(pady=5)

        btn = ctk.CTkButton(win, text="Salvar Alteração", command=lambda: self.salvar_edicao_emp(id_emp, entry_dev.get(), win))
        btn.pack(pady=20)

    def salvar_edicao_emp(self, id_emp, nova_data, win):
        try:
            nova_data = date.fromisoformat(nova_data)
        except:
            messagebox.showerror("Erro", "Data inválida (use AAAA-MM-DD)")
            return
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE Emprestimos set data_devolucao=%s WHERE id_emprestimo=%s", (nova_data, id_emp))

        conn.commit()
        conn.close()
        self.carregar_emprestimos()
        win.destroy()
        messagebox.showinfo("Sucesso", "Empréstimo atualizado!")

    def deletar_emprestimo(self):
        item = self.tree_emp.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um Empréstimo para Deletar")
            return
        else:
            id_emp = self.tree_emp.item(item, "values") [0]
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Emprestimo WHERE id_emprestimo=%s", (id_emp,))
        
        conn.commit()
        conn.close()
        self.carregar_emprestimos()
        messagebox.showinfo("Sucesso", "Empréstimo deletado com sucesso")

    def salvar_emprestimo(self, cliente_str, livro_str, win):
        if not cliente_str or not livro_str:
            messagebox.showwarning("Aviso", "Selecione Cliente e Livro")
            return
        id_cliente = (cliente_str.split(" - ")[0])
        id_livro = (livro_str.split(" - ")[0])

        # Gera ID do empréstimo no automáticamente aleatório no formato E123
        id_emprestimo = gerar_id_unico("Emprestimos", "id_emprestimo")

        hoje = date.today()
        devolucao = hoje + timedelta(days=7)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Emprestimos (id_emprestimo, id_cliente, id_livro, data_emprestimo, data_devolucao) VALUES (%s,%s,%s,%s,%s)", (id_emprestimo, id_cliente, id_livro, hoje, devolucao)
        )

        conn.commit()
        conn.close()
        self.carregar_emprestimos()
        win.destroy()
        messagebox.showinfo("Sucesso", f"Empréstimo cadastrado com ID: {id_emprestimo}!")


    # ============================== HELPERS ==============================

    def get_clientes(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nome_cliente FROM Cliente WHERE status='Ativo'")
        dados = cursor.fetchall()
        conn.close()
        return dados

    def get_livros(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_livro, titulo_livro FROM Livro WHERE status='Ativo'")
        dados = cursor.fetchall()
        conn.close()
        return dados

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ============================== RESUMO ==============================

    def frame_resumo(self):
        self.clear_main()
        lbl = ctk.CTkLabel(self.main_frame, text="Resumo da Biblioteca", font=("Arial", 18))
        lbl.pack(pady=20)

        conn = conectar()
        cursor = conn.cursor()


        # Últimos Livros
        lbl1 = ctk.CTkLabel(self.main_frame, text="Últimos Livros Cadastrados:")
        lbl1.pack()

        # Tabela
        tree1 = ttk.Treeview(self.main_frame, columns=("Título", "Autor", "Ano"), show="headings", height=5)
        tree1.pack(pady=5, padx=10, fill="x")

        for col in ("Título", "Autor", "Ano"):
            tree1.heading(col, text=col)
        cursor.execute("SELECT titulo_livro, autor_livro, ano FROM Livro ORDER BY id_livro DESC LIMIT 5")

        for row in cursor.fetchall():
            tree1.insert("", "end", values=row)

        # Livros mais emprestados
        lbl2 = ctk.CTkLabel(self.main_frame, text="\nLivros mais emprestados")
        lbl2.pack()

        tree2 = ttk.Treeview(self.main_frame, columns=("Título", "Qtd"), show="headings", height=5)
        tree2.pack(pady=5, padx=10, fill="x")
        tree2.heading("Título", text="Título")
        tree2.heading("Qtd", text="Qtd")

        cursor.execute("""
        SELECT
            l.titulo_livro,
            COUNT(e.id_livro) as total FROM Emprestimos e
            JOIN Livro l ON e.id_livro = l.id_livro
            GROUP BY l.titulo_livro ORDER BY total DESC LIMIT 5""")
        for row in cursor.fetchall():
            tree2.insert("", "end", values=row)

        # Devoluções próximas
        lbl3 = ctk.CTkLabel(self.main_frame, text="\nDevoluções próximas (7 Dias)")
        lbl3.pack()
        tree3 = ttk.Treeview(self.main_frame, columns=("Cliente", "Livro", "Devolução"), show="headings", height=5)
        tree3.pack(pady=5, padx=10, fill="x")

        for col in ("Cliente", "Livro", "Devolução"):
            tree3.heading(col, text=col)

        cursor.execute("""
            SELECT
                c.nome_cliente,
                l.titulo_livro,
                e.data_devolucao
            FROM Emprestimos e
            JOIN Cliente c ON e.id_cliente = c.id_cliente
            JOIN Livro l ON e.id_livro = l.id_livro 
            WHERE e.data_devolucao IS NOT NULL AND e.data_devolucao <= %s""", (date.today() + timedelta(days=7),))
        for row in cursor.fetchall():
            tree3.insert("", "end", values=row)

        conn.close()

if __name__ == "__main__":
    app = Biblioteca()
    app.mainloop()