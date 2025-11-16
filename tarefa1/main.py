from ca_manager import create_root_ca, create_intermediate_ca, issue_certificate

root_ca, root_key = create_root_ca()
intermediate_ca, inter_key = create_intermediate_ca(root_ca, root_key)
server_cert = issue_certificate(intermediate_ca, inter_key)
