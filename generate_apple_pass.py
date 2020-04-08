from passes_generator.apple_passes import generator, resources

if __name__ == "__main__":
    pass_res = {
  "formatVersion": 1,
  "passTypeIdentifier": "pass.com.ssoboy",
  "serialNumber": "ART",
  "teamIdentifier": "WSULUSUQ63",
  "webServiceURL": "https://example.com/passes/",
  "authenticationToken": "vxwxd7J8AlNNFPS8k0a0FfUFtq0ewzFdc",
  "barcode": {
    "message": "db64999a-d280-4b5f-895c-038cf92c1ab2",
    "format": "PKBarcodeFormatQR",
    "messageEncoding": "iso-8859-1"
  },
  "locations": [
    {
      "longitude": -122.3748889,
      "latitude": 37.6189722
    },
    {
      "longitude": -122.03118,
      "latitude": 37.33182
    }
  ],

"organizationName":"org","description":"descr","labelColor":"rgb(0, 98, 255)","logoText":"ЛогоТекст","foregroundColor":"rgb(255, 249, 240)","backgroundColor":"rgb(119, 217, 100)","backFields":[],"storeCard":{"headerFields":[{"key":"_676325044","label":"ХедерЛейбл","value":"ХедерВалуе"}],"primaryFields":[{"key":"_768436380","label":"Главный лейбл","value":"Главное"}],"secondaryFields":[{"key":"_988064272","label":"ВторЛейбл","value":"ВторВалуе"},{"key":"_378698882","label":"Привет","value":"Мир"}],"auxiliaryFields":[{"key":"_860322443","label":"ВспомЛейбл","value":"ВспомВалуе"}]}

}

    apple_resource_object = resources.ApplePassResources(pass_res)
    apple_pass_generator = generator.ApplePassKitGenerator(
        resource=apple_resource_object
    )
    file_names = ["icon.png", "icon@2x.png", "logo.png"]

    for file_name in file_names:
        file = open("apple_pass_images/" + file_name, "rb")
        apple_pass_generator.add_file(file_name, file.read())
    buffer = apple_pass_generator.create()
    with open("LoyaltyCard.pkpass", "wb") as f:
        f.write(buffer.read())
