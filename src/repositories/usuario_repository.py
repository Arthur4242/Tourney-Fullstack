from models.usuario import Usuario
from sqlalchemy.orm import Session
from sqlalchemy import select

class UsuarioRepository:

    def __init__(self, session: Session):
        self.session = session

    def listar(self):
        return self.session.query(Usuario).all()
    
    def busar_usuario_por_id(self, usuario_id: int) -> Usuario | None:
        return self.session.get(Usuario, usuario_id)
    
    def busar_usuario_por_email(self, usuario_email: str) -> Usuario | None:
        stmt = select(Usuario).where(Usuario.email == usuario_email)
        return self.session.scalar(stmt)
    
    
    def adicionar_usuario(self, usuario) -> Usuario:

        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)

        return usuario
    
    
    def deletar_usuario(self, usuario: Usuario) -> None:
        
        self.session.delete(usuario)
        self.session.commit()
        return True
    
    def salvar(self, usuario: Usuario) -> Usuario:
        self.session.commit()
        self.session.refresh(usuario)
        return usuario