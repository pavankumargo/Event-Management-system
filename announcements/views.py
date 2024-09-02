from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Student,Clubs,Events,club_members,event_students,events_pics
# Create your views here.
"""
Clubs.objects.create(club_id='ptm100',club_name='Prayatnam',club_description='welcome')
Clubs.objects.create(club_id='dnd100',club_name='Dance and Dramatics',club_description='welcome')
Clubs.objects.create(club_id='pnp100',club_name='Painting and Photography',club_description='welcome')
Clubs.objects.create(club_id='lnd100',club_name='Literary and Debate',club_description='welcome')
Clubs.objects.create(club_id='air100',club_name='AI and Robotics',club_description='welcome')
Clubs.objects.create(club_id='eyn100',club_name='E-Yantra',club_description='welcome')
Clubs.objects.create(club_id='ctm100',club_name='Chitram',club_description='welcome')

club_members.objects.create(club_id='ptm100',stu_id=420117)
club_members.objects.create(club_id='ptm100',stu_id=420248)
club_members.objects.create(club_id='lnd100',stu_id=720132)
club_members.objects.create(club_id='lnd100',stu_id=420137)
club_members.objects.create(club_id='pnp100',stu_id=420117)
club_members.objects.create(club_id='ctm100',stu_id=420248)

User.objects.create(username='ptm100',password='Qwerty@1234',email='prayatnam@nitandhra.ac.in')
User.objects.create(username='dnd100',password=1234,email='danceanddramatics@nitandhra.ac.in')
User.objects.create(username='pnp100',password=1234,email='photography@nitandhra.ac.in')
User.objects.create(username='lnd100',password=1234,email='literaryanddebate@nitandhra.ac.in')
User.objects.create(username='air100',password=1234,email='aiandrobotics@nitandhra.ac.in')
User.objects.create(username='eyn100',password=1234,email='eyantra@nitandhra.ac.in')
User.objects.create(username='ctm100',password=1234,email='chitram@nitandhra.ac.in')
"""


def home(request):
    ev=Events.objects.filter(status='in progress')
    context={
        'ev':ev
    }
    return render(request,'home.html',context)
def register(request):
    if request.method== 'POST':
        roll=request.POST['rollno']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        phone=request.POST['mobile']
        dept=request.POST['dept']
        cgpa=request.POST['cgpa']
        year=request.POST['year']
        password=request.POST['password']
        if len(request.FILES)!=0:
            myfile=request.FILES['pic']
            Student.objects.create(roll_no=roll,email=email,first_name=first_name,last_name=last_name,
                                    dept_name=dept,year=year,phone=phone,cgpa=cgpa,pic=myfile)
        Student.objects.create(roll_no=roll,email=email,first_name=first_name,last_name=last_name,
                                    dept_name=dept,year=year,phone=phone,cgpa=cgpa)
        user=User.objects.create_user(username=roll,password=password,email=email,first_name=first_name)
        user.save()
        return redirect('login')
    else:
        return render(request,'register.html')

def login(request):
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['roll']=username
            return redirect('slogin')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

def slogin(request):
    roll=request.session['roll']
    st=Student.objects.get(roll_no=roll)
    ev=Events.objects.filter(status='in progress')
    context={
        'st' :st,
        'ev':ev
    }
    return render(request,'stdhome.html',context)



def dashboard(request):
    roll=request.session['roll']
    es=event_students.objects.filter(stu_id=roll)
    st=Student.objects.get(roll_no=roll)
    ev=[]
    for e in es:
        x=Events.objects.get(event_id=e.event_id)
        if x.status=="in progress":
            ev.append(x)
    context={
        'ev':ev,
        'st':st,
    }
    return render(request,'dashboard.html',context)


def logout(request):
    auth.logout(request)
    return redirect('/')

def club(request,club_id):
    cl=Clubs.objects.get(club_id=club_id)
    st=club_members.objects.filter(club_id=club_id)
    ev=Events.objects.filter(club_id=club_id,status='in progress')
    evc=Events.objects.filter(club_id=club_id,status='complete')
    evp=events_pics.objects.filter(club_id=club_id)
    stus=[]
    for s in st:
        a=[]
        a.append(Student.objects.get(roll_no=s.stu_id))
        a.append(s.position)
        stus.append(a)
    
    context={
        'cl':cl,
        'stus':stus,
        'ev':ev,
        'evp':evp,
        'evc':evc,
    }
    return render(request,'clubs.html',context)


def club_login(request):
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['cl']=username
            return redirect('clogin')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('club_login')
    else:
        return render(request,'club_login.html')


def create_event(request,club_id):
    if request.method=='POST':
        name=request.POST['name']
        des=request.POST['description']
        dat=request.POST['date']
        time=request.POST['time']
        ven=request.POST['venue']
        cl=Clubs.objects.get(club_id=club_id)
        e=Events.objects.create(club_id=club_id,club_name=cl.club_name,name=name,task=des)
        if len(request.FILES)!=0:
            myfile=request.FILES['poster']
            e.poster=myfile
        if dat:
            e.date=dat
        if time:
            e.time=time
        if ven:
            e.venue=ven
        e.save();
        return redirect('clogin')
    else:
        return render(request,'create_event.html',{'club_id':club_id})

def clogin(request):
    username=request.session['cl']
    cl=Clubs.objects.get(club_id=username)
    evp=Events.objects.filter(club_id=username,status='in progress')
    evc=Events.objects.filter(club_id=username,status='complete')
    mem=club_members.objects.filter(club_id=username)
    mems=[]
    for m in mem:
        a=[]
        a.append(Student.objects.get(roll_no=m.stu_id))
        a.append(m.position)
        mems.append(a)
    context={
        'cl':cl,
        'evc':evc,
        'evp':evp,
        'mems':mems
    }    
    return render(request,'club_home.html',context)

def event_register(request,event_id):
    roll=request.session['roll']
    evs=event_students.objects.filter(event_id=event_id,stu_id=roll).first()
    if evs is None:
        event_students.objects.create(event_id=event_id,stu_id=roll)
    else:
        messages.info(request,'Already registered.')
    return redirect('slogin')

def edit_details(request):
    return render(request,'update_details.html')

def upd_stu(request) :
    roll=request.session['roll']
    st=Student.objects.get(roll_no=roll)
    user = User.objects.get(username=roll)
    fname = request.POST['first_name']
    lname = request.POST['last_name']
    cgpa = request.POST['cgpa']
    password = request.POST['password']
    phone = request.POST['phone']
    year=request.POST['year']
    if 'update' in request.POST:
        if fname :
            st.first_name=fname
        if lname :
            st.last_name=lname
        if cgpa:
            st.cgpa = cgpa
        if password :
            user.set_password(password)
        if phone :
            st.phone=phone
        if year:
            st.year=year
        if len(request.FILES)!=0:
            myfile=request.FILES['myfile']
            st.pic=myfile
        st.save();
        user.save();
        return redirect('slogin')
    else:
        return redirect('slogin')

def add_member(request):
    if request.method=='POST':
        club_id=request.session['cl']
        roll=request.POST['rollno']
        pos=request.POST['position']
        club_members.objects.create(club_id=club_id,stu_id=roll,position=pos)
        return redirect('clogin')
    else:
        return render(request,'add_member.html')


def mark_complete(request,event_id):
    ev=Events.objects.get(event_id=event_id)
    ev.status="complete"
    ev.save();
    return redirect('clogin')


def view_details(request,event_id):
    students=event_students.objects.filter(event_id=event_id)
    s=[]
    for stu in students:
        s.append(Student.objects.get(roll_no=stu.stu_id))
    ev=Events.objects.get(event_id=event_id)
    context={
        'st':s,
        'e':ev,
    }
    
    return render(request,'details.html',context)


def uppic(request,event_id):
    request.session['ev']=event_id
    return redirect('upload_pic')

def upload_pic(request):
    if request.method== 'POST':
        club_id=request.session['cl']
        event_id=request.session['ev']
        e=Events.objects.get(event_id=event_id)
        if len(request.FILES)!=0:
            pics=request.FILES['pic']
        events_pics.objects.create(club_id=club_id,event_name=e.name,pic=pics)
        return redirect('clogin')
    else:
        return render(request,'upload_pic.html')


def upd_event(request,event_id) :
    if request.method=='POST':
        e=Events.objects.get(event_id=event_id)
        name=request.POST['name']
        des=request.POST['description']
        dat=request.POST['date']
        time=request.POST['time']
        ven=request.POST['venue']
        if 'update' in request.POST:
            if len(request.FILES)!=0:
                myfile=request.FILES['poster']
                e.poster=myfile
            if dat:
                e.date=dat
            if time:
                e.time=time
            if ven:
                e.venue=ven
            if des:
                e.task=des
            e.save();
            return redirect('clogin')
        else:
            return redirect('clogin')
    else:
        return render(request,'update_event.html',{'event_id':event_id})