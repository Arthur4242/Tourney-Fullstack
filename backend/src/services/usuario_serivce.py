from backend.src.models.usuario import Usuario
from backend.src.repositories.usuario_repository import UsuarioRepository
import re

class UsuarioService:
   
    EMAIL_REGEX = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )
    
    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def _validar_email(self, email):
        # if not email:
        #     raise ValueError("O e-mail é obrigatório.")

        if not self.EMAIL_REGEX.fullmatch(email):
            raise ValueError("E-mail inválido.")

    def listarUsuarios(self):
        return self.usuario_repository.listar()

    def cadastrarUsuario(self, nome: str, email: str | None = None):
        
        if email:
            self._validar_email(email)

            if self.usuario_repository.busar_usuario_por_email(email):
                raise ValueError("Este email já possui um cadastro.")
        
        usuario = Usuario(
            nome = nome,
            email = email
        )

        return self.usuario_repository.adicionar_usuario(usuario)
    
    def buscarUsuarioPorId(self, usuario_id: int):
        usuario = self.usuario_repository.busar_usuario_por_id(usuario_id)
        if usuario is None:
            raise ValueError("Usuario não encontrado.")
        return usuario

    def buscarUsuarioPorEmail(self, email: str):
        usuario = self.usuario_repository.busar_usuario_por_email(email)
        if usuario is None:
            raise ValueError("Usuario não encontrado.")
        return usuario
    
    def atualizarUsuario(self, id: int, nome: str | None = None, email: str | None = None):
        usuario = self.buscarUsuarioPorId(id)

        if nome:
            usuario.nome = nome
        if email:
            self._validar_email(email)
            usuario.email = email
        return self.usuario_repository.salvar(usuario)

    def deletarUsuario(self, usuario):
        if usuario is None:
            raise ValueError("Usuario não encontrado")
        
        self.usuario_repository.deletar_usuario(usuario)
