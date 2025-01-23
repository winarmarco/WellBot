def get_contact_psychologist() -> str:
    psychologists = [
        {
            "name": "Dr. Alice Carter",
            "description": "Clinical psychologist specializing in cognitive-behavioral therapy (CBT) for anxiety, depression, and trauma-related disorders.",
            "phone number": "+1-555-123-4567",
            "email": "alice.carter@example.com",
            "location": "New York, NY, USA",
            "gender": "Female",
        },
        {
            "name": "Dr. Mark Johnson",
            "description": "Licensed psychologist focused on family counseling, couples therapy, and conflict resolution.",
            "phone number": "+1-555-987-6543",
            "email": "mark.johnson@example.com",
            "location": "Los Angeles, CA, USA",
            "gender": "Male",
        },
        {
            "name": "Dr. Emily Nguyen",
            "description": "Expert in adolescent psychology and emotional regulation, specializing in ADHD and academic-related stress.",
            "phone number": "+1-555-234-5678",
            "email": "emily.nguyen@example.com",
            "location": "Seattle, WA, USA",
            "gender": "Female",
        },
        {
            "name": "Dr. James Foster",
            "description": "Specialist in grief counseling, post-traumatic stress disorder (PTSD), and emotional resilience building.",
            "phone number": "+1-555-876-5432",
            "email": "james.foster@example.com",
            "location": "Chicago, IL, USA",
            "gender": "Male",
        },
        {
            "name": "Dr. Sophia Martinez",
            "description": "Child psychologist experienced in developmental disorders, behavioral therapy, and autism spectrum interventions.",
            "phone number": "+1-555-345-6789",
            "email": "sophia.martinez@example.com",
            "location": "Miami, FL, USA",
            "gender": "Female",
        },
    ]

    # Parse all the psychologiest object in the form of
    #
    # {Psychologist Name}
    # - {field 1}: {value 1}
    # - {field 2}: {value 2}
    # - {field 3}: {value 3}
    # - {field 4}: {value 4}
    psychologist_profiles = []
    for psychologist in psychologists:
        profile = [f"### {psychologist['name']}"]
        for field, value in psychologist.items():
            if field != "name":  # Skip name since we used it as header
                profile.append(f"- {field}: {value}")
        psychologist_profiles.append("\n".join(profile))

    psychologist_profile_prompt = "\n\n".join(psychologist_profiles)
    system_prompt = f"""
      If you detect a mental health emergency or crisis situation, here are qualified mental health professionals who can provide immediate assistance. Please contact the professional nearest to your location:

      {psychologist_profile_prompt}

      In case of immediate danger to yourself or others, please call emergency services based on the location of the user immediately.
      """

    return system_prompt
