from ca_manager import create_root_ca, create_intermediate_ca, issue_certificate

# Criação da CA Raiz
root_ca, root_key = create_root_ca()

# Criação da CA Intermediária, assinada pela CA Raiz
intermediate_ca, inter_key = create_intermediate_ca(root_ca, root_key)

# Criação do Certificado de servidor, assinado pela CA Intermediária
server_cert = issue_certificate(intermediate_ca, inter_key)
