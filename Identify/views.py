from .models import Contact
from .serializers import ContactSerializer
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def identify_contact(request):
    data = request.data
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')

    # Check if there is an existing primary contact with the given email or phoneNumber
    primary_contact = Contact.objects.filter(
        (Q(email=email) | Q(phoneNumber=phoneNumber)) &
        (Q(linkPrecedence='primary') | Q(linkPrecedence='secondary'))
    ).first()

    if not primary_contact:
        # If there is no existing primary contact, create a new one
        primary_contact = Contact.objects.create(
            email=email,
            phoneNumber=phoneNumber,
            linkPrecedence='primary'
        )
    else:
        secondary_contacts=Contact.objects.create(email=email,
            phoneNumber=phoneNumber,
            linkPrecedence='secondary',
            linkedId=primary_contact.id
        )

    # Identify secondary contacts linked to the primary contact
    secondary_contacts = Contact.objects.filter(linkedId=primary_contact.id)
    
    # Extract data from primary and secondary contacts
    secondary_emails = [contact.email for contact in secondary_contacts]
    secondary_phone_numbers = [contact.phoneNumber for contact in secondary_contacts]
    secondary_contact_ids = [contact.id for contact in secondary_contacts]
    
    # Serialize the primary contact and return the consolidated contact data
    serialized_contact = ContactSerializer(primary_contact).data

    # Return the consolidated contact data in JSON response
    return Response({
        "contact": {
            "primaryContatctId": serialized_contact['id'],
            "emails": set([serialized_contact['email']] + secondary_emails),
            "phoneNumbers": set([serialized_contact['phoneNumber']] + secondary_phone_numbers),
            "secondaryContactIds": secondary_contact_ids,
        }
    })


@api_view(['GET'])
def all_contacts(request):
    if request.method == 'GET':
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "Only GET requests are supported."}, status=400)
    
