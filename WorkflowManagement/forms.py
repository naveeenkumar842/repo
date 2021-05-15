from django import forms
from .models import NewWorkflowManagement, UserDataWorkflowManagement
from django.contrib.auth import get_user_model
from .choices import Element_Type, validations
from django.forms import formset_factory
from string import Template
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core import validators
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


alphanumeric = validators.RegexValidator(r'^[0-9a-zA-Z ]*$', 'Only alphanumeric characters are allowed.')


class NewWorkflowManagementForm(forms.Form):
    name = forms.CharField(label=_('Workflow Name :'),max_length=30,validators=[alphanumeric], widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder': _('Enter Workflow Name here'),'autocomplete':'off' }))


class WorkflowManagement(forms.Form):
    label = forms.CharField(label=_('Label'),validators=[alphanumeric], widget=forms.TextInput(attrs={'class':'form-control form-control-sm','autocomplete':'off' }))
    element_type = forms.ChoiceField(label=_('Element Type'), choices=Element_Type, initial='Select Element', widget=forms.Select(attrs={'class':'form-control form-control-sm' }))
    validation = forms.ChoiceField(label=_('Validations'), choices=validations, widget=forms.Select(attrs={'class':'form-control form-control-sm'}))


WorkflowManagementFormset = formset_factory(WorkflowManagement, extra=1)


class WorkflowFormView(forms.Form):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        from django.core import validators
        import re

        self._queryset_id = kwargs.pop('queryset_id', None)
        super(WorkflowFormView, self).__init__(*args, **kwargs)

        jsonData = NewWorkflowManagement.objects.get(id=self._queryset_id)
        jsonData = jsonData.wf_definition

        alphanumeric = validators.RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

        only_alphabets = validators.RegexValidator(r'^[a-zA-Z]*$', 'Only Alphabets are allowed.')

        def checkmobile(value):
            Pattern = re.compile("(0/91/022)?[7-9][0-9]{9}")
            if not Pattern.match(value):
                raise forms.ValidationError("Invalid Mobile Number")

        def validateEmail(email):
            from django.core.validators import validate_email
            from django.core.exceptions import ValidationError
            try:
                validate_email(email)
                return True
            except ValidationError:
                raise forms.ValidationError("Email Address not Valid")

        def validate_pan_number(value):
            if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', value):
                pass
            else:
                raise forms.ValidationError("Invalid Pan Number")

        def only_digits(value):
            if re.match(r'^ *\d[\d ]*$', value):
                pass
            else:
                raise forms.ValidationError("Only Digits Allowed")
        def validate_aadhar_number(value):
            if re.match(r'^\d{12}$', value):
                pass
            else:
                raise forms.ValidationError("Invalid Aadhar Number")

        for json in jsonData:
            if json['element_type'] == 'TextField' and json['validation'] == 'alphanumeric':
                if json['required']==True:
                    self.fields[json['label']] = forms.CharField(max_length=50, validators=[alphanumeric],required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-sm alpha-num'}))
                else:
                    self.fields[json['label']] = forms.CharField(max_length=50, validators=[alphanumeric],required=False,
                                                                 widget=forms.TextInput(
                                                                     attrs={'class': 'form-control form-control-sm alpha-num'}))

            elif json['element_type'] == 'TextField' and json['validation'] == 'only numbers':
                if json['required']==True:
                    self.fields[json['label']] = forms.CharField(max_length=50, validators=[only_digits],required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
                else:
                    self.fields[json['label']] = forms.CharField(max_length=50, validators=[only_digits],required=False,widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
            elif json['element_type'] == 'TextField' and json['validation'] == 'only_alphabets':
                if json['required'] == True:
                    self.fields[json['label']] = forms.CharField(max_length=50, validators=[only_alphabets],required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-sm alpha'}))
                else:
                    self.fields[json['label']] = forms.CharField(max_length=50, validators=[only_alphabets],required=False,
                                                                 widget=forms.TextInput(
                                                                     attrs={'class': 'form-control form-control-sm alpha'}))
            elif json['element_type'] == 'TextField' and json['validation'] == 'email':
                if json['required'] == True:
                    self.fields[json['label']] = forms.CharField(max_length=50, validators=[validateEmail],required=True,widget=forms.TextInput(attrs={'id': 'email_validate', 'class':'form-control form-control-sm email_validate'}))
                else:
                    self.fields[json['label']] = forms.CharField(max_length=50, validators=[validateEmail],required=False,
                                                                 widget=forms.TextInput(attrs={'id': 'email_validate',
                                                                                               'class': 'form-control form-control-sm email_validate'}))
            elif json['element_type'] == 'TextField' and json['validation'] == 'checkmobile':
                if json['required'] == True:
                    self.fields[json['label']] = forms.CharField(max_length=10, validators=[checkmobile],required=True,
                                                             widget=forms.TextInput(attrs={'id': 'mobile_id', 'class':'form-control form-control-sm mobile_id'}))
                else:
                    self.fields[json['label']] = forms.CharField(max_length=10, validators=[checkmobile],required=False,
                                                                 widget=forms.TextInput(attrs={'id': 'mobile_id',
                                                                                               'class': 'form-control form-control-sm mobile_id'}))

            elif json['element_type'] == 'TextField' and json['validation'] == 'pancard_validation':
                if json['required'] == True:
                    self.fields[json['label']] = forms.CharField(max_length=10, validators=[validate_pan_number],required=True,widget=forms.TextInput(attrs={'id': 'pan_id', 'class':'form-control form-control-sm pan_id'}))
                else:
                    self.fields[json['label']] = forms.CharField(max_length=10, validators=[validate_pan_number],required=False,
                                                                 widget=forms.TextInput(attrs={'id': 'pan_id',
                                                                                               'class': 'form-control form-control-sm pan_id'}))

            elif json['element_type'] == 'TextField' and json['validation'] == 'aadhar_validation':
                if json['required'] == True:
                    self.fields[json['label']] = forms.CharField(max_length=12, validators=[validate_aadhar_number],required=True,widget=forms.TextInput(attrs={'id': 'aadhar_id', 'class':'form-control form-control-sm aadhar_id'}))
                else:
                    self.fields[json['label']] = forms.CharField(max_length=12, validators=[validate_aadhar_number],required=False,
                                                                 widget=forms.TextInput(attrs={'id': 'aadhar_id',
                                                                                               'class': 'form-control form-control-sm aadhar_id'}))

            elif json['element_type'] == 'TextField' and json['validation'] == 'No Validation':
                if json['required'] == True:
                    self.fields[json['label']] = forms.CharField(max_length=50 ,required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
                else:
                    self.fields[json['label']] = forms.CharField(max_length=50,required=False, widget=forms.TextInput(
                        attrs={'class': 'form-control form-control-sm'}))

            elif json['element_type'] == 'TextField' and json['validation'] == 'email':
                if json['required'] == True:
                    self.fields[json['label']] = forms.CharField(max_length=20,required=True, widget=forms.TextInput(attrs={'id': 'email_validate' ,'class':'form-control form-control-sm email_validate'}))
                else:
                    self.fields[json['label']] = forms.CharField(max_length=20,required=False, widget=forms.TextInput(
                        attrs={'id': 'email_validate', 'class': 'form-control form-control-sm email_validate'}))
            elif json['element_type'] == 'TextArea':
                if json['required'] == True:
                    self.fields[json['label']] = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class':'form-control form-control-sm'}))
                else:
                    self.fields[json['label']] = forms.CharField(required=False,
                        widget=forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control form-control-sm'}))

            elif json['element_type'] == 'RadioButton':
                if json['required'] == True:
                    self.fields[json['label']] = forms.CharField(required=True,widget=forms.RadioSelect(choices=json['element_names']))
                else:
                    self.fields[json['label']] = forms.CharField(required=False,
                        widget=forms.RadioSelect(choices=json['element_names']))

            elif json['element_type'] == 'CheckBox':
                if json['required'] == True:
                    self.fields[json['label']] = forms.CharField(required=True,widget=forms.CheckboxSelectMultiple(choices=json['element_names']))
                else:
                    self.fields[json['label']] = forms.CharField(required=False,
                        widget=forms.CheckboxSelectMultiple(choices=json['element_names']))
            elif json['element_type'] == 'ChoiceField':
                if json['required'] == True:
                    self.fields[json['label']] = forms.ChoiceField(choices=json['element_names'],required=True,widget=forms.Select())
                else:
                    self.fields[json['label']] = forms.ChoiceField(choices=json['element_names'],required=False,
                                                                   widget=forms.Select())
            elif json['element_type'] == 'FileField':
                if json['required'] == True:
                    self.fields[json['label']] = forms.ImageField(required=True,widget=forms.FileInput(attrs={'class': 'form-control form-control-sm lbl_image'}))
                else:
                    self.fields[json['label']] = forms.ImageField(required=False,
                        widget=forms.FileInput(attrs={'class': 'form-control form-control-sm lbl_image'}))


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html = Template("""<img src="$link" width='150', hieght='150'/>""")
        return mark_safe(html.substitute(media=settings.MEDIA_URL, link=value))


class MakerWorkflowFormView(forms.Form):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        from django.core import validators
        import re

        self._queryset_id = kwargs.pop('queryset_id', None)
        super(MakerWorkflowFormView, self).__init__(*args, **kwargs)

        user_data = UserDataWorkflowManagement.objects.get(id=self._queryset_id)
        if user_data.f_entry == "Y":
            jsonData1 = user_data.new_user_data_definition
            form_jsonData = user_data.workflow_id.new_wf_definition
        else:
            jsonData1 = user_data.user_data_definition
            form_jsonData = user_data.workflow_id.wf_definition

        # print('form_jsonData', form_jsonData)

        newJsonData = {}
        for i in jsonData1:
            newJsonData = i

        alphanumeric = validators.RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
        only_alphabets = validators.RegexValidator(r'^[a-zA-Z]*$', 'Only Alphabets are allowed.')

        def validateEmail(email):
            from django.core.validators import validate_email
            from django.core.exceptions import ValidationError
            try:
                validate_email(email)
                return True
            except ValidationError:
                raise forms.ValidationError("Email Address not Valid")

        def checkmobile(value):
            Pattern = re.compile("(0/91/022)?[7-9][0-9]{9}")
            if not Pattern.match(value):
                raise forms.ValidationError("Invalid Mobile Number")

        def validate_pan_number(value):
            if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', value):
                pass
            else:
                raise forms.ValidationError("Invalid Pan Number")

        def only_digits(value):
            if re.match(r'^ *\d[\d ]*$', value):
                pass
            else:
                raise forms.ValidationError("Only Digits Allowed")

        def validate_aadhar_number(value):
            if re.match(r'^\d{12}$', value):
                pass
            else:
                raise forms.ValidationError("Invalid Aadhar Number")

        for p,q in newJsonData.items():
            # print(p, q)
            for j in form_jsonData:
                if j['label'] == p:
                    if j['element_type'] == 'TextField' and j['validation'] == 'alphanumeric':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(max_length=50,required=True, validators=[alphanumeric], widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
                        else:
                            self.fields[j['label']] = forms.CharField(max_length=50,required=False, validators=[alphanumeric], widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
                        
                    elif j['element_type'] == 'TextField' and j['validation'] == 'only numbers':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(max_length=50, validators=[only_digits],required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
                        else:
                            self.fields[j['label']] = forms.CharField(max_length=50, validators=[only_digits],required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

                    elif j['element_type'] == 'TextField' and j['validation'] == 'only_alphabets':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(max_length=50,required=True, validators=[only_alphabets], widget=forms.TextInput(attrs={'class':'form-control form-control-sm alpha'}))
                        else:
                            self.fields[j['label']] = forms.CharField(max_length=50,required=False, validators=[only_alphabets], widget=forms.TextInput(attrs={'class':'form-control form-control-sm alpha'}))
                        
                    elif j['element_type'] == 'TextField' and j['validation'] == 'email':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(max_length=50,required=True, validators=[validateEmail],widget=forms.TextInput(attrs={'id': 'email_validate', 'class':'form-control form-control-sm email_validate'}))
                        else:
                            self.fields[j['label']] = forms.CharField(max_length=50,required=False, validators=[validateEmail],widget=forms.TextInput(attrs={'id': 'email_validate', 'class':'form-control form-control-sm email_validate'}))
                        
                    elif j['element_type'] == 'TextField' and j['validation'] == 'pancard_validation':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(max_length=10,required=True, validators=[validate_pan_number],widget=forms.TextInput(attrs={'id': 'pan_id', 'class':'form-control form-control-sm pan_id'}))
                        else:
                            self.fields[j['label']] = forms.CharField(max_length=10,required=False, validators=[validate_pan_number],widget=forms.TextInput(attrs={'id': 'pan_id', 'class':'form-control form-control-sm pan_id'}))
                        
                    elif j['element_type'] == 'TextField' and j['validation'] == 'checkmobile':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(max_length=10, validators=[checkmobile],required=True,
                                                                             widget=forms.TextInput(attrs={'id': 'mobile_id', 'class':'form-control form-control-sm mobile_id'}))
                        else:
                            self.fields[j['label']] = forms.CharField(max_length=10, validators=[checkmobile],required=False,
                                                                             widget=forms.TextInput(attrs={'id': 'mobile_id', 'class':'form-control form-control-sm mobile_id'}))
                        
                    elif j['element_type'] == 'TextField' and j['validation'] == 'aadhar_validation':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(max_length=12, validators=[validate_aadhar_number],required=True,
                                                                     widget=forms.TextInput(attrs={'id': 'aadhar_id', 'class':'form-control form-control-sm aadhar_id'}))
                        else:
                            self.fields[j['label']] = forms.CharField(max_length=12, validators=[validate_aadhar_number],required=False,
                                                                     widget=forms.TextInput(attrs={'id': 'aadhar_id', 'class':'form-control form-control-sm aadhar_id'}))
                        
                    elif j['element_type'] == 'TextField' and j['validation'] == 'No Validation':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(max_length=50,required=True, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
                        else:
                            self.fields[j['label']] = forms.CharField(max_length=50,required=False, widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
                            
                    elif j['element_type'] == 'TextField' and j['validation'] == 'email':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(max_length=20,required=True, widget=forms.TextInput(attrs={'id': 'email_validate', 'class':'form-control form-control-sm email_validate'}))
                        else:
                            self.fields[j['label']] = forms.CharField(max_length=20,required=False, widget=forms.TextInput(attrs={'id': 'email_validate', 'class':'form-control form-control-sm email_validate'}))
                            
                    elif j['element_type'] == 'TextArea':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class':'form-control form-control-sm'}))
                        else:
                            self.fields[j['label']] = forms.CharField(required=False,widget=forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class':'form-control form-control-sm'}))
                        
                    elif j['element_type'] == 'RadioButton':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(required=True,widget=forms.RadioSelect(choices=j['element_names']))
                        else:
                            self.fields[j['label']] = forms.CharField(required=False,widget=forms.RadioSelect(choices=j['element_names']))
                        
                    elif j['element_type'] == 'CheckBox':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.CharField(required=True,widget=forms.CheckboxSelectMultiple(choices=j['element_names']))
                        else:
                            self.fields[j['label']] = forms.CharField(required=False,widget=forms.CheckboxSelectMultiple(choices=j['element_names']))
                        
                    elif j['element_type'] == 'ChoiceField':
                        if j['required'] == True:
                            self.fields[j['label']] = forms.ChoiceField(choices=j['element_names'],required=True, widget=forms.Select())
                        else:
                            self.fields[j['label']] = forms.ChoiceField(choices=j['element_names'],required=False, widget=forms.Select())


class MakerWorkflowFormView2(forms.Form):

    def __init__(self, *args, **kwargs):

        self._queryset_id = kwargs.pop('queryset_id', None)
        super(MakerWorkflowFormView2, self).__init__(*args, **kwargs)

        user_data = UserDataWorkflowManagement.objects.get(id=self._queryset_id)
        jsonData1 = user_data.user_data_definition

        form_jsonData = user_data.workflow_id.wf_definition

        for i in jsonData1:
            newJsonData = i

        for p,q in newJsonData.items():
            for j in form_jsonData:
                if j['label'] == p:
                    if j['element_type'] == 'FileField':
                        self.fields[j['label']] = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control lbl_image'}))


class UserDataWorkflowManagementForm(forms.ModelForm):
    # Choices = (
    #     ('', '--Select--'),
    #     ('Approved', _('Approved')),
    #     ('Rejected', _('Rejected')),
    # )
    # status = forms.ChoiceField(label=_('Status'), choices=Choices,  initial='No Validation')
    remarks = forms.CharField(label=_('Remarks'))
    class Meta:
        model = UserDataWorkflowManagement
        fields = ('remarks',)
        widgets = {
            'remarks': forms.Textarea(attrs={'class':'form-control','rows': 4, 'cols': 20, 'required':True}),
            # 'status': forms.Select(attrs={'class':'form-group'}),
        }


class ScanDocumentForm(forms.Form):
    selected_device = forms.CharField(label=_('Selected Device'))


class SelectTaggingInfo(forms.Form):
    CHOICES = [('Application Form', 'Application Form'),
            ('Aadhar Card', 'Aadhar Card'),
            ('Pan Card', 'Pan Card'),
            ('Driving License', 'Driving License'),
            ('Signature', 'Signature'),
            ('Photo', 'Photo')]

    account_saving = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)




class FinnacleAccountForm(forms.Form):
    choices = (
        ('yes', 'Yes'),
        ('no', 'No')
    )

    new_choices = (
        ('Required', 'Required'),
        ('Not Required', 'Not Required')
    )

    Account_Number = forms.CharField(label=_('Account Number'), widget=forms.TextInput(
        attrs={'name': 'FORACID', 'class': "form-control form-control-sm"}))
    Application_Number = forms.CharField(label=_('Application Number'),
                                         widget=forms.TextInput(attrs={'class': "form-control form-control-sm"}))
    ACCT_OPN_DATE = forms.CharField(label=_('ACCT_OPN_DATE'),
                                    widget=forms.TextInput(attrs={'class': "form-control form-control-sm"}))
    SCHM_CODE = forms.CharField(label=_('SCHM_CODE'),
                                widget=forms.TextInput(attrs={'class': "form-control form-control-sm"}))
    SCHM_TYPE = forms.CharField(label=_('SCHM_TYPE'),
                                widget=forms.TextInput(attrs={'class': "form-control form-control-sm"}))
    SOL_ID = forms.CharField(label=_('SOL_ID'),
                             widget=forms.TextInput(attrs={'class': "form-control form-control-sm"}))
    IB_Facility_required = forms.ChoiceField(label=_('IB Facility required'), required=True, choices=choices,
                                             widget=forms.Select())
    IB_QR_code_required = forms.ChoiceField(label=_('IB QR code required'), required=True, choices=choices,
                                            widget=forms.Select())

    Document_Download = forms.ChoiceField(label=_('Document Download'), required=False, choices=new_choices,
                                          widget=forms.Select())



class MisQueryFormWorkflow(forms.Form):
    CHOICE = (
        ('Select', 'Select'),
        ('PDF', 'PDF'),
        ('Excel', 'Excel')
              )

    def selectvalue(value):

        if value == 'Select':
            raise forms.ValidationError("Please select a format to Export data")

    choice_field = forms.ChoiceField(label=_('Export To'),required=True,choices=CHOICE, validators=[selectvalue], widget=forms.Select())
    query = forms.CharField(label=_('Query'),required=True, widget=forms.Textarea(attrs={'rows': 8, 'cols': 50}))

class workflowform(forms.ModelForm):
    f=forms.CharField(label=_('From'))
    t=forms.CharField(label=_('To'))
    workflow_number = forms.CharField(label=_('workflow_number'))
    class Meta:
        model = UserDataWorkflowManagement
        fields = ['workflow_number']