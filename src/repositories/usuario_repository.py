from models.usuario import Usuario
from sqlalchemy.orm import Session

class UsuarioRepository:

    def __init__(self, session: Session):
        self.session = session

    def listar(self):
        return self.session.query(Usuario).all()
    
    def busar_usuario_por_id(self, usuario_id: int) -> Usuario | None:
        return self.session.get(Usuario, usuario_id)
    
    def adicionarUsuario(self, nome: str, email: str | None = None) -> Usuario:
        usuario = Usuario(
            nome = nome,
            email = email
        )

        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)

        return usuario
    
    
    def deletarUsuario(self, usuario_id) -> None:
        usuario = self.busar_usuario_por_id(usuario_id)

        if usuario is None:
            return False
        
        self.session.delete(usuario)
        self.session.commit()
        return True
    
    def salvar(self, usuario: Usuario) -> Usuario:
        self.session.commit()
        self.session.refresh(usuario)
        return usuario