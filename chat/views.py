from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from account.models import User, recruiter, jobSeeker
from .models import messages

# Create your views here.
@login_required
def index(request):
    template_data = {}
    template_data['title'] = 'Messages'
    template_data['is_index'] = True
    
    # Get all unique conversations for the current user
    conversations = []
    
    if request.user.is_job_seeker:
        # Get job seeker profile
        try:
            jobseeker_profile = jobSeeker.objects.get(user=request.user)
            # Find all unique recruiters this job seeker has messaged with
            unique_conversations = messages.objects.filter(
                jobSeekerIDFK=jobseeker_profile
            ).values('recruiterIDFK').distinct()
            
            for conv in unique_conversations:
                recruiter_profile = recruiter.objects.get(id=conv['recruiterIDFK'])
                last_message = messages.objects.filter(
                    jobSeekerIDFK=jobseeker_profile,
                    recruiterIDFK=recruiter_profile
                ).order_by('-timestamp').first()

                if last_message and last_message.sender:
                    preview_sender = 'you' if last_message.sender_id == request.user.id else recruiter_profile.user.username
                    preview_message = last_message.message[:100]
                    if len(last_message.message) > 100:
                        preview_message += '...'
                    is_unread = last_message.sender_id != request.user.id and not last_message.read_by_jobseeker
                else:
                    preview_sender = recruiter_profile.user.username
                    preview_message = ''
                    is_unread = False
                
                conversations.append({
                    'other_user': recruiter_profile.user,
                    'last_message': last_message,
                    'preview_sender': preview_sender,
                    'preview_message': preview_message,
                    'is_unread': is_unread,
                    'url': f"/messages/{request.user.username}/{recruiter_profile.user.username}/"
                })
        except jobSeeker.DoesNotExist:
            pass
    
    elif request.user.is_recruiter:
        # Get recruiter profile
        try:
            recruiter_profile = recruiter.objects.get(user=request.user)
            # Find all unique job seekers this recruiter has messaged with
            unique_conversations = messages.objects.filter(
                recruiterIDFK=recruiter_profile
            ).values('jobSeekerIDFK').distinct()
            
            for conv in unique_conversations:
                jobseeker_profile = jobSeeker.objects.get(id=conv['jobSeekerIDFK'])
                last_message = messages.objects.filter(
                    recruiterIDFK=recruiter_profile,
                    jobSeekerIDFK=jobseeker_profile
                ).order_by('-timestamp').first()

                if last_message and last_message.sender:
                    preview_sender = 'you' if last_message.sender_id == request.user.id else jobseeker_profile.user.username
                    preview_message = last_message.message[:100]
                    if len(last_message.message) > 100:
                        preview_message += '...'
                    is_unread = last_message.sender_id != request.user.id and not last_message.read_by_recruiter
                else:
                    preview_sender = jobseeker_profile.user.username
                    preview_message = ''
                    is_unread = False
                
                conversations.append({
                    'other_user': jobseeker_profile.user,
                    'last_message': last_message,
                    'preview_sender': preview_sender,
                    'preview_message': preview_message,
                    'is_unread': is_unread,
                    'url': f"/messages/{request.user.username}/{jobseeker_profile.user.username}/"
                })
        except recruiter.DoesNotExist:
            pass
    
    # Sort conversations by last message timestamp (most recent first)
    conversations.sort(key=lambda x: x['last_message'].timestamp if x['last_message'] else None, reverse=True)
    
    template_data['conversations'] = conversations
    template_data['show_select_conversation'] = True
    
    return render(request, 'chat/index.html', {'template_data': template_data})

@login_required
def chat_room(request, user1_username, user2_username):
    template_data = {}
    template_data['title'] = 'Messages'
    
    user1 = get_object_or_404(User, username=user1_username)
    user2 = get_object_or_404(User, username=user2_username)
    
    # Validate that the current user is one of the two users in the conversation
    if request.user not in [user1, user2]:
        django_messages.error(request, "You don't have permission to view this conversation.")
        return redirect('chat.index')
    
    # Determine which user is the recruiter and which is the job seeker
    if user1.is_recruiter and user2.is_job_seeker:
        recruiter_user = user1
        jobseeker_user = user2
    elif user1.is_job_seeker and user2.is_recruiter:
        recruiter_user = user2
        jobseeker_user = user1
    else:
        django_messages.error(request, "Invalid conversation participants.")
        return redirect('chat.index')
    
    # Validate URL structure: first user should be the logged-in user
    if request.user.username != user1_username:
        # Redirect to correct URL format
        return redirect('chat.room', user1_username=request.user.username, user2_username=user2_username)
    
    recruiter_profile = get_object_or_404(recruiter, user=recruiter_user)
    jobseeker_profile = get_object_or_404(jobSeeker, user=jobseeker_user)
    
    # Handle sending a new message
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            sender_is_recruiter = request.user.id == recruiter_user.id
            messages.objects.create(
                recruiterIDFK=recruiter_profile,
                jobSeekerIDFK=jobseeker_profile,
                sender=request.user,
                read_by_recruiter=sender_is_recruiter,
                read_by_jobseeker=not sender_is_recruiter,
                message=message_text
            )
            return redirect('chat.room', user1_username=request.user.username, user2_username=user2_username)

    if request.user.is_recruiter:
        messages.objects.filter(
            recruiterIDFK=recruiter_profile,
            jobSeekerIDFK=jobseeker_profile,
            read_by_recruiter=False
        ).exclude(sender=request.user).update(read_by_recruiter=True)
    elif request.user.is_job_seeker:
        messages.objects.filter(
            recruiterIDFK=recruiter_profile,
            jobSeekerIDFK=jobseeker_profile,
            read_by_jobseeker=False
        ).exclude(sender=request.user).update(read_by_jobseeker=True)
    
    # Get messages between these two users
    conversation = messages.objects.filter(
        recruiterIDFK=recruiter_profile,
        jobSeekerIDFK=jobseeker_profile
    ).order_by('timestamp')

    if request.user.is_recruiter:
        latest_seen_by_other = messages.objects.filter(
            recruiterIDFK=recruiter_profile,
            jobSeekerIDFK=jobseeker_profile,
            sender=request.user,
            read_by_jobseeker=True
        ).order_by('-timestamp').first()
    else:
        latest_seen_by_other = messages.objects.filter(
            recruiterIDFK=recruiter_profile,
            jobSeekerIDFK=jobseeker_profile,
            sender=request.user,
            read_by_recruiter=True
        ).order_by('-timestamp').first()
    
    template_data['recruiter'] = recruiter_profile
    template_data['jobseeker'] = jobseeker_profile
    template_data['conversation'] = conversation
    template_data['other_user'] = user2
    template_data['current_user_id'] = request.user.id
    template_data['latest_seen_message_id'] = latest_seen_by_other.id if latest_seen_by_other else None
    template_data['is_chat_room'] = True
    
    return render(request, 'chat/index.html', {'template_data': template_data})