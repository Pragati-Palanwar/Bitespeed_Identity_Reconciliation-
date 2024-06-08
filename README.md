Bitespeed Reconcillation Solution

Language : Python
Framework : Django
Database : sqlite
Tool : Postman


I have design a web service with an endpoint /identify that will receive HTTP POST requests with JSON body of the following format:

{
"email"?: string,
"phoneNumber"?: number
}

We need to set Postman HTTP request with POST method and url "http://127.0.0.1:8000/app/identify/" then web service returns a HTTP 200 response with a JSON payload containing the consolidated contact in this format:

{
"contact":{
"primaryContatctId": number,
"emails": string[], // first element being email of primary contact
"phoneNumbers": string[], // first element being phoneNumber of primary contact
"secondaryContactIds": number[] // Array of all Contact IDs that are "secondaryContacts"
}
}


If an incoming request has either of phoneNumber or email common to an existing contact but contains new information, the service will create a “secondary” Contact row.

If we want to know all primary and secondary contacts details of our user then set a Postman HTTP request with GET method and url "http://127.0.0.1:8000/app/all-contacts/". 
Even we can see primary contacts turn into secondary within it.
