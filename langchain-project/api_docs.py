import json

dialog_api_docs = {
    "base_url" : "http://127.0.0.1:5000/",
    "endponts" : {
        # "/register_status" : {
        #     "methods" : "POST",
        #     "description" : "Registers a new user if the NIC is not already in the JSON.",
        #     "parameters" : None,
        #     "response" : {
        #         "description" : "A JSON object containing already registered users details",
        #         "content_type" : "application/json"
        #     }
        # },
        
        "/list" : {
            "methods" : "GET",
            "description" : "Retrieve the list of connections and packages for mobile broadband, home broadband and dialog tv",
            "parameters" : None,
            "response" : {
                "description" : "A JSON object containing available connections and packeges and along with their package types",
                "content_type" : "application/json"
            }
        },
        
        "/special_offers" :{
            "methods" : "GET",
            "description" : "Retrieve current special offers and discounts.",
            "parameters" : None,
            "response" : {
                "description" : "A JSON object listing the current special offers and discounts.",
                "content_type" : "application/json"
            }
        },
        
        "/new_package" :{
            "methods" : "GET",
            "description" : "Retrieve new introduced packages",
            "parameters" : None,
            "response" : {
                "description" : "A JSON object listing the newly introduced packages",
                "content_type" : "application/json"
            }
        },
        # "/customer-reviews" :{
        #     "methods" : "GET",
        #     "description" : "Retrieve customer reviews for the ice cream store.",
        #     "parameter" : None,
        #     "response" : {
        #         "description" : "A JSON object containing customer reviews, ratings, and comments.",
        #         "content_type" : "application/json"
        #     }
        # },
        # "/customizations" : {
        #     "methods" : "GET",
        #     "description" : "Retrieve available ice cream customizations.",
        #     "parameters" : None,
        #     "response" : {
        #         "description" : "A JSON object listing available customizations like toppings and sugar-free options.",
        #         "content_type" : "application/json"
        #     }
        # }
    }  
}
# Convert the dictionary to a JSON string
dialog_api_docs = json.dumps(dialog_api_docs, indent=2)