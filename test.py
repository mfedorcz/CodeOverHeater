import polyline

# Encoded polyline string
encoded_polyline = "kcp_IktspAHJFFFBB@H@B@H?J?HCLC@AHGDGBADIDMDSJ_@HQDIFGDEFAHAHAN@L?dCRX@"

# Decode the polyline string
decoded_coordinates = polyline.decode(encoded_polyline)

# Print the decoded coordinates
print(decoded_coordinates)