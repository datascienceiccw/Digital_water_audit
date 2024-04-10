from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .models import (
    SourceWaterProfile,
    RainWaterProfile,
    FreshWaterTreatmentProfile,
    FreshWaterTreatmentMethods,
    BasicDetails,
    FreshWaterTreatmentProfileDetails,
    SourceWaterFlow,
    TanksCapacities,
    TanksCapacitiesSource,
    DrinkingWaterSource,
    DrinkingWaterSystem,
    DrinkingWaterSourceName,
    RestaurantConsumption,
    KitchenDishwasherTapConsumption,
    BanquetConsumption,
    BanquetSource,
    GuestRoomConsumption,
    GuestRoomDomesticSource,
    GuestRoomToiletSource,
    EmployeeRoomConsumption,
    EmployeeRoomDomesticSource,
    EmployeeRoomToiletSource,
    DriversRoomConsumption,
    DriversRoomDomesticSource,
    DriversRoomToiletSource,
    SwimmingPoolConsumption,
    SwimmingPoolSource,
    WaterBodiesConsumption,
    WaterBodiesSource,
    LaundryConsumption,
    LaundrySource,
    BoilerConsumption,
    BoilerSource,
    BoilerTreatmentMethods,
    AddBoilerConsumption,
    CalorifierConsumption,
    CalorifierSource,
    CoolingTowerConsumption,
    AddCoolingTowerConsumption,
    AddCoolingTowerSource,
    IrrigationConsumption,
    IrrigationSource,
    OtherConsumption,
    OtherConsumptionSource,
    WasteWaterTreatment,
    WasteWaterTreatmentSTP,
    WasteWaterTreatmentETP,
    WasteWaterTreatmentOthers,
    TanksAndCapacities,
    TanksAndCapacitiesSource,
    WaterQualityProfile,
    RecycledWaterProfile,
)
from .forms import (
    RegistrationForm,
    BasicDetailsForm,
    SourceWaterProfileForm,
    SourceWaterFlowForm,
    RainWaterProfileForm,
    FreshWaterTreatmentProfileForm,
    FreshWaterTreatmentProfileDetailsForm,
    TanksCapacitiesForm,
    KitchenDishwasherTapConsumptionForm,
    DrinkingWaterSourceForm,
    RestaurantConsumptionForm,
    BanquetConsumptionForm,
    GuestRoomConsumptionForm,
    EmployeeRoomConsumptionForm,
    DriversRoomConsumptionForm,
    SwimmingPoolConsumptionForm,
    WaterBodiesConsumptionForm,
    LaundryConsumptionForm,
    BoilerConsumptionForm,
    BoilerTreatmentMethodsForm,
    AddBoilerConsumptionForm,
    CalorifierConsumptionForm,
    CoolingTowerConsumptionForm,
    AddCoolingTowerConsumptionForm,
    IrrigationConsumptionForm,
    OtherConsumptionForm,
    WasteWaterTreatmentForm,
    WasteWaterTreatmentSTPForm,
    WasteWaterTreatmentETPForm,
    WasteWaterTreatmentOthersForm,
    TanksAndCapacitiesForm,
    WaterQualityProfileForm,
    RecycledWaterProfileForm,
)

from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
import json
import plotly
import plotly.graph_objs as go
from .dash_source_app import create_user_dash_app
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from django.forms import modelformset_factory


def home_view(request):
    if request.user.is_authenticated:
        return redirect("user_home")
    if request.method == "POST":
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("registration_done/")
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, "home.html", {"form": form})


@login_required
def user_home_view(request):
    if not request.session.get("message_seen", False):
        messages.success(request, "")
        request.session["message_seen"] = True
    return render(request, "user_home.html", {"user": request.user})


@login_required
def logout_view(request):
    logout(request)
    # if not request.session.get("message_seen", False):
    #     messages.success(request, "")
    #     request.session["message_seen"] = True
    return HttpResponseRedirect("/")


@login_required
def basic_details(request):  # sourcery skip: assign-if-exp, merge-else-if-into-elif
    current_user = request.user
    details = BasicDetails.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = BasicDetailsForm(request.POST or None, initial={'organization_type':'Hospitality'})
        if form.is_valid():
            form.instance.user = current_user
            form.save()
            return redirect("source-water-profile/")
        else:
            print(form.errors)
    else:
        if details:
            form = BasicDetailsForm(instance=details)
        else:
            form = BasicDetailsForm()
    return render(request, "BasicDetails.html", {"form": form, "details": details})


@login_required
def delete_basic_details(request):
    current_user = request.user
    BasicDetails.objects.filter(user=current_user).delete()
    return redirect("basic_details")


@login_required
def source_water_profile(request):
    if request.method == "POST":
        form = SourceWaterProfileForm(request.POST)
        if form.is_valid():
            current_user = request.user
            form.instance.user = current_user
            names = request.POST.getlist('source_name')
            other_source_name = request.POST.getlist('other_source_name')
            consumptions = request.POST.getlist('source_daily_consumption')
            cost = request.POST.getlist('source_water_cost')
            if names and consumptions and cost:
                for i in range(len(names)):
                    if names[i] == 'Others':
                        source_water_profile = SourceWaterProfile.objects.create(user=current_user, source_name=other_source_name[0], source_daily_consumption=consumptions[i], source_water_cost=cost[i])
                        other_source_name = other_source_name[1:]
                    else:    
                        source_water_profile = SourceWaterProfile.objects.create(user=current_user, source_name=names[i], source_daily_consumption=consumptions[i], source_water_cost=cost[i])
                    source_water_profile.save()
            return redirect("source_water_profile")
        else:
            print(form.errors)
    else:
        form = SourceWaterProfileForm()
    all_sources = SourceWaterProfile.objects.filter(user=request.user)
    return render(
        request, "SourceWaterProfile.html", {"form": form, "all_sources": all_sources}
    )


@login_required
def delete_source_water_profile(request):
    current_user = request.user
    SourceWaterProfile.objects.filter(user=current_user).delete()
    return redirect("source_water_profile")


@login_required
def rainwater(request):  # sourcery skip: assign-if-exp, merge-else-if-into-elif
    current_user = request.user
    details = RainWaterProfile.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = RainWaterProfileForm(request.POST or None)
        if form.is_valid():
            form.instance.user = current_user
            form.save()
            return redirect("source_dash_view")
        else:
            print(form.errors)
    else:
        if details:
            form = RainWaterProfileForm(instance=details)
        else:
            form = RainWaterProfileForm()
    is_rainwater_present = SourceWaterProfile.objects.filter(
        user=current_user, source_name=4
    ).exists()
    print(is_rainwater_present)
    return render(
        request,
        "rainwater.html",
        {
            "form": form,
            "details": details,
            "is_rainwater_present": is_rainwater_present,
        },
    )


@login_required
def delete_rainwater(request):
    current_user = request.user
    RainWaterProfile.objects.filter(user=current_user).delete()
    return redirect("rainwater_details")


@login_required
def fresh_water_treatment_profile(request):
    global treatment_methods
    treatment_methods = []
    current_user = request.user
    if request.method == "POST":
        form = FreshWaterTreatmentProfileForm(request.POST)
        if form.is_valid():
            freshwater_treatment = form.save(commit=False)
            freshwater_treatment.user = current_user
            # freshwater_treatment.save()

            other_treatment = form.cleaned_data['name']
            for name in other_treatment:
                print(name)
                name = name.strip()
                if name:
                    treatment_profile = FreshWaterTreatmentProfile.objects.create(user=current_user, name=name)
                    treatment_profile.save()
                    # FreshWaterTreatmentProfile.objects.get_or_create(name=name)

            other_treatment = request.POST.getlist('other_sources')
            if other_treatment:
                for name in other_treatment:
                    treatment_profile = FreshWaterTreatmentProfile.objects.create(user=current_user, name=name)
                    treatment_profile.save()   
                    # FreshWaterTreatmentProfile.objects.get_or_create(name=name)  
            return redirect("fresh_water_treatment_profile")
        else:
            print(form.errors)
    else:
        form = FreshWaterTreatmentProfileForm()

    treatment_methods.clear()
    all_treatment_methods = FreshWaterTreatmentProfile.objects.filter(user=request.user)
    for method in all_treatment_methods:
        treatment_methods.append(method)
    return render(
        request,
        "FreshWaterTreatmentProfile.html",
        {"form": form, "all_treatment_methods": all_treatment_methods},
    )


@login_required
def delete_fresh_water_treatment_profile(request):
    current_user = request.user
    FreshWaterTreatmentProfile.objects.filter(user=current_user).delete()
    return redirect("fresh_water_treatment_profile")


@login_required
def fresh_water_treatment_profile_details(request):
    profiles = FreshWaterTreatmentProfile.objects.filter(user=request.user)
    if request.method == "POST":
        if "reset" in request.POST:
            profile_id_to_reset = request.POST["reset"]
            print(profile_id_to_reset)
            FreshWaterTreatmentProfileDetails.objects.filter(
                profile_id=profile_id_to_reset
            ).delete()
        else:
            for profile in profiles:
                form = FreshWaterTreatmentProfileDetailsForm(
                    request.POST, prefix=str(profile.id)
                )
                if form.is_valid():
                    details = form.save(commit=False)
                    details.profile = profile
                    details.save()
        return redirect("fresh_water_treatment_profile_details")
    forms = {}
    for profile in profiles:
        details = FreshWaterTreatmentProfileDetails.objects.filter(
            profile=profile
        ).first()

        if details:
            form = FreshWaterTreatmentProfileDetailsForm(
                prefix=str(profile.id), instance=details
            )
        else:
            form = FreshWaterTreatmentProfileDetailsForm(prefix=str(profile.id))

        if profile.name not in [
            "Pressure Sand Filter(PSF)or Multi Grade Filter(MGF)",
            "Iron Removal Filters(IRF)",
            "Activated Carbon Filter (ACF)",
            "Softener",
            "Ultrafiltration(UF)",
        ]:
            if "backwash_time" in form.fields:
                del form.fields["backwash_time"]

            if "rinse_time" in form.fields:
                del form.fields["rinse_time"]

        if profile.name != "Reverse Osmosis(RO)" and "flush_time" in form.fields:
            del form.fields["flush_time"]

        if profile.name != "Softener" and "regeneration_time" in form.fields:
            del form.fields["regeneration_time"]

        if profile.name != "Softener":
            if "frequency_of_regeneration" in form.fields:
                del form.fields["frequency_of_regeneration"]

            if "amount_of_water_for_brine_solution" in form.fields:
                del form.fields["amount_of_water_for_brine_solution"]

        if (
            profile.name
            not in [
                "Pressure Sand Filter(PSF)or Multi Grade Filter(MGF)",
                "Iron Removal Filters(IRF)",
                "Activated Carbon Filter (ACF)",
                "Softener",
                "Ultrafiltration(UF)",
            ]
            and "frequency_of_backwash_and_rinse" in form.fields
        ):
            del form.fields["frequency_of_backwash_and_rinse"]

        forms[profile] = {"form": form, "details": details}
    total_treatment_profile_details = len(
        FreshWaterTreatmentProfileDetails.objects.all()
    )

    all_form_filled = total_treatment_profile_details == len(profiles)
    context = {"forms": forms, "all_form_filled": all_form_filled}

    return render(request, "FreshWaterTreatmentProfileDetails.html", context)


@login_required
def thank_you_view(request, *args, **kwargs):
    return render(request, "thank_you.html", {})


def fresh_water_details_charts():
    # Fetching data from the database
    details = FreshWaterTreatmentProfileDetails.objects.select_related("profile").all()
    profile_names = [detail.profile.name for detail in details]
    input_water = [detail.input_water for detail in details]
    product_water = [detail.product_water for detail in details]
    reject_water = [detail.reject_water for detail in details]

    # Bar Chart: Water Input vs. Product Water vs Reject Water
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=profile_names, y=input_water, name="Input Water"))
    fig1.add_trace(go.Bar(x=profile_names, y=product_water, name="Product Water"))
    fig1.add_trace(go.Bar(x=profile_names, y=reject_water, name="Reject Water"))

    fig1.update_layout(
        title_text="Water Input vs Product Water",
        title_font=dict(
            size=20, family="Arial, sans-serif", color="navy"
        ),  # Title font settings
        paper_bgcolor="rgba(0,0,0,0.1)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
        legend=dict(
            # Semi-transparent legend background
            bgcolor="rgba(255, 255, 255, 0.6)",
            bordercolor="Black",
            borderwidth=2,
        ),
        autosize=True,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )

    return json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)


@login_required
def source_water_pie_chart(request):
    current_user = request.user

    # Aggregating daily water consumption by source type
    aggregation = (
        SourceWaterProfile.objects.filter(user=current_user)
        .values("source_name")
        .annotate(total=Sum("source_daily_consumption"))
    )

    # Creating a dictionary to hold the consumption values for each source
    consumption = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    for item in aggregation:
        consumption[item["source_name"]] += item["total"]

    # Extracting the values and converting them into a list
    borewell_volume = consumption["1"]
    tanker_volume = consumption["2"]
    metro_volume = consumption["3"]
    rain_volume = consumption["4"]
    others_volume = consumption["5"]

    total_input_water = sum(
        [borewell_volume, tanker_volume, metro_volume, rain_volume, others_volume]
    )
    if total_input_water == 0:
        return render(
            request, "error_page.html", {"error": "No Water Consumption Data"}
        )

    labels = ["Borewell", "Tanker", "Metro", "Rain", "Others"]
    values = [borewell_volume, tanker_volume, metro_volume, rain_volume, others_volume]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                hoverinfo="label+percent+value",
                hovertemplate="%{label}: %{value} litres<br><extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title_text="Water Consumption Share",  # Title
        title_font=dict(
            size=20, family="Arial, sans-serif", color="navy"
        ),  # Title font settings
        paper_bgcolor="rgba(0,0,0,0.1)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
        legend=dict(
            # Semi-transparent legend background
            bgcolor="rgba(255, 255, 255, 0.6)",
            bordercolor="Black",
            borderwidth=2,
        ),
        autosize=True,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fresh_water_details_input_reject_product_bar = fresh_water_details_charts()

    context = {
        "graph_json": graph_json,
        "total_input_water": total_input_water,
        "borewell_volume": borewell_volume,
        "tanker_volume": tanker_volume,
        "metro_volume": metro_volume,
        "rain_volume": rain_volume,
        "others_volume": others_volume,
        "fresh_water_details_input_reject_product_bar": fresh_water_details_input_reject_product_bar,
    }

    return render(request, "water_chart.html", context)


# previous implementation of flowchart_view using mermaid.js
# @login_required
# def flowchart_view(request):  # sourcery skip: dict-comprehension
#     current_user = request.user
#     source_water_profile = SourceWaterProfile.objects.filter(
#         user=current_user).all()
#     treatment_profile = FreshWaterTreatmentProfile.objects.filter(
#         user=current_user).all()
#     treatment_profile_seq_dic = {}
#     for treatment in treatment_profile:
#         treatment_profile_seq_dic[treatment.sequence_number] = treatment.name
#     mermaid_code = generate_mermaid_code(
#         current_user, source_water_profile, treatment_profile_seq_dic)

#     return render(request, 'flowchart.html', {'mermaid_code': mermaid_code})

# def source_water_mermaid_content(source_water_profile):
#     source_water_mermaid = """
#     style subgraphcontent fill:black,stroke:#333
#     subgraph subgraphcontent[<b> </b>]"""

#     # A dictionary to map source names for the Mermaid diagram
#     source_names = {
#         '1': 'Borewell Water',
#         '2': 'Tanker Water',
#         '3': 'Metro Water',
#         '4': 'Rain Water',
#         '5': 'Others'
#     }

#     # Iterate over each source water profile entry
#     for source in source_water_profile:
#         source_name = source_names.get(source.source_name, "Unknown")
#         source_consumption = source.source_daily_consumption
#         if source_consumption > 0:
#             source_water_mermaid += f'\n    style {source.source_name} fill:#1ca3ec,stroke:black,stroke-width:2px;'
#             source_water_mermaid += f'\n    {source.source_name}[({source_name})] -->|{source_consumption} kl| A[Total Source Water]'

#     source_water_mermaid += '''\nend \n'''
#     return source_water_mermaid


# def get_total_source_water(current_user):
#     source_water_profiles = SourceWaterProfile.objects.filter(user=current_user)
#     total_input_water = sum(profile.source_daily_consumption for profile in source_water_profiles)
#     return total_input_water


# def get_input_reject_water_from_treatments(current_user):
#     treatment_profiles = FreshWaterTreatmentProfile.objects.filter(
#         user=current_user).all()
#     dic = {}
#     for treatment in treatment_profiles:
#         dic[treatment.name] = (float(treatment.details.input_water), float(
#             treatment.details.reject_water))
#     return dic


# def fresh_water_treatment_mermaid_content(current_user, seq_dict):
#     total_source_water = get_total_source_water(current_user)
#     input_reject_dic = get_input_reject_water_from_treatments(current_user)
#     fresh_water_treatment_mermaid = """
#     style subgraphcontent1 fill:black,stroke:#333
#     subgraph subgraphcontent1[<b> </b>]\n
#     """
#     prev_node = 'A'
#     fresh_water_treatment_mermaid += f'   style {prev_node} fill:green,stroke:black,stroke-width:2px;\n'
#     fresh_water_treatment_mermaid += f'   {prev_node} --> |{total_source_water} kl| '

#     for key, value in sorted(seq_dict.items()):
#         main_node = chr(66 + key - 1)  # ASCII character starting from 'B'
#         # Additional node connected to each main node
#         aux_node = f'A{main_node}'

#         # Add main node and connect it to the auxiliary node
#         fresh_water_treatment_mermaid += f'{main_node}("{value}") -->|{input_reject_dic[value][1]} kl| {aux_node}("Reject")\n'
#         fresh_water_treatment_mermaid += f'style {aux_node} fill:red,stroke:black,stroke-width:2px;'
#         # Connect to the next main node if not the last key
#         if key != max(seq_dict.keys()):
#             next_main_node = chr(66 + key)
#             fresh_water_treatment_mermaid += f'   {main_node} --> |{input_reject_dic[value][0]} kl| {next_main_node}\n'
#             print(next_main_node)
#         else:
#           fresh_water_treatment_mermaid += f' {main_node} --> |{input_reject_dic[value][0]} kl| K[Tanks]\n'
#           fresh_water_treatment_mermaid += f'style K fill:green,stroke:black,stroke-width:2px;'


#     fresh_water_treatment_mermaid += '\nend'
#     return fresh_water_treatment_mermaid

# def generate_mermaid_code(current_user, source_water_profile, treatment_profile_seq_dic):
#     mermaid_code = """
#     graph TB;
#     style A fill:gray,stroke:black,stroke-width:2px;
#     """

#     mermaid_code += source_water_mermaid_content(source_water_profile)
#     mermaid_code += fresh_water_treatment_mermaid_content(
#         current_user, treatment_profile_seq_dic)
#     # print(mermaid_code)
#     return mermaid_code


def get_source_water(user):
    sources = SourceWaterProfile.objects.filter(user=user)
    # Manual construction of data to include get_source_name_display
    sources_data = [
        {
            "id": source.id,
            "name": source.get_source_name_display(),
            "consumption": source.source_daily_consumption,
        }
        for source in sources
    ]

    # Serialize the manually constructed list of dictionaries to JSON
    return json.dumps(sources_data)


def get_freshwater_treatment(user):
    treatments = FreshWaterTreatmentProfile.objects.filter(user=user)
    treatments_data = [
        {
            "id": treatment.id,
            "name": treatment.name,
            "seq_number": treatment.id,
            "input_water": str(treatment.details.input_water),
            "product_water": str(treatment.details.product_water),
            "reject_water": str(treatment.details.reject_water),
        }
        for treatment in treatments
    ]

    return json.dumps(treatments_data)


@login_required
def flowchart_view(request):
    user = request.user
    sources_json = get_source_water(user)
    treatements_json = get_freshwater_treatment(user)

    context = {
        "sources": sources_json,
        "treatments": treatements_json,
    }
    return render(request, "flowchart.html", context)


@login_required
def tanks_capacities(request):
    tank_names = ['Input freshwater tank',
                'Fire tank',
                'Softener Storage tank',
                'RO Storage tank',
                'Flush tank',
                'Domestic Water tank',
                'RO Input tank',
                'Boiler Makeup tank',
                'Others']
    current_user = request.user
    if request.method == "POST":
        form = TanksCapacitiesForm(request.POST)
        if form.is_valid():
            form.instance.user = current_user
            names = request.POST.getlist('name')
            capacities = request.POST.getlist('capacity')
            other_tank_name = request.POST.getlist('other_tank_name')
            if names and capacities:
                for i in range(len(names)): 
                    if names[i] == 'Others':
                        tank_capacity = TanksCapacities.objects.create(user=current_user, name=other_tank_name[0], capacity=capacities[i]) 
                        other_tank_name = other_tank_name[1:]
                    else:    
                        tank_capacity = TanksCapacities.objects.create(user=current_user, name=names[i], capacity=capacities[i])
                    tank_capacity.save()    
            return redirect("tanks_capacities")
        else:
            print(form.errors)
    else:
        form = TanksCapacitiesForm()

    all_tanks = TanksCapacities.objects.filter(user=request.user)
    return render(
        request, "TanksCapacities.html", {"form": form, "all_tanks": all_tanks, 'tank_names': tank_names}
    )


@login_required
def delete_tanks_capacities(request):
    current_user = request.user
    TanksCapacities.objects.filter(user=current_user).delete()
    return redirect("tanks_capacities")





@login_required
def source_water_flow(request):
    existing_entries = SourceWaterFlow.objects.filter(user=request.user).exists()
    extra_forms = 0 if existing_entries else 1

    SourceWaterFlowFormSet = modelformset_factory(SourceWaterFlow, form=SourceWaterFlowForm, extra=extra_forms, can_delete=True)

    # Fetching all sources and destinations from the database
    fresh_water_sources = SourceWaterProfile.objects.filter(user=request.user)
    treatment_methods = FreshWaterTreatmentProfile.objects.filter(user=request.user)
    tanks = TanksCapacities.objects.filter(user=request.user)

    sources = [(source.id, source.source_name) for source in fresh_water_sources] + \
              [(method.id, method.name) for method in treatment_methods] + \
              [(tank.id, tank.name) for tank in tanks]

    destinations = [(method.id, method.name) for method in treatment_methods] + \
                   [(tank.id, tank.name) for tank in tanks]


    if 'reset' in request.POST:
        SourceWaterFlow.objects.filter(user=request.user).delete()
        existing_entries = False
        return redirect('source_water_flow')

    if request.method == "POST" and not existing_entries:
        formset = SourceWaterFlowFormSet(
            request.POST,
            request.FILES,
            queryset=SourceWaterFlow.objects.none(),
            form_kwargs={'sources': sources, 'destinations': destinations}
        )
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.source and instance.destination and instance.volume:
                    instance.user = request.user
                    instance.save()
            existing_entries = True
            return redirect('source_water_flow')

    formset = SourceWaterFlowFormSet(
        queryset=SourceWaterFlow.objects.filter(user=request.user) if existing_entries else SourceWaterFlow.objects.none(),
        form_kwargs={'sources': sources, 'destinations': destinations}
    )

    return render(request, "SourceWaterFlow.html", {
        'formset': formset,
        'existing_entries': existing_entries
    })


@login_required
def delete_source_water_flow(request):
    current_user = request.user
    SourceWaterFlow.objects.filter(user=current_user).delete()
    return redirect('source-destination')


@login_required
def kitchen_consumption_view(request):
    current_user = request.user
    all_details = KitchenDishwasherTapConsumption.objects.filter(user=current_user)
    details = KitchenDishwasherTapConsumption.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = KitchenDishwasherTapConsumptionForm(request.POST)
        if form.is_valid():
            kitchen_consumption = form.save()
            kitchen_consumption.user = request.user
            kitchen_consumption.save()
            return redirect("kitchen_consumption")
    else:
        form = KitchenDishwasherTapConsumptionForm()
    return render(
        request,
        "KitchenConsumption.html",
        {
        "form": form, 
        # "details": details,
         "all_details": all_details}
        ,
    )


@login_required
def delete_kitchen_consumption(request):
    current_user = request.user
    KitchenDishwasherTapConsumption.objects.filter(user=current_user).delete()
    return redirect("kitchen_consumption")


@login_required
def delete_kitchen(request, kitchen_id):
    # Get the restaurant object to delete
    kitchen = get_object_or_404(KitchenDishwasherTapConsumption, id=kitchen_id)
    # Delete the restaurant
    kitchen.delete()

    return redirect("kitchen_consumption")


@login_required
def drinking_water_source_view(request):
    current_user = request.user
    details = DrinkingWaterSource.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = DrinkingWaterSourceForm(request.POST)
        if form.is_valid():
            drinking_water = form.save(commit=False)
            drinking_water.user = current_user
            drinking_water.save()

            source_names = form.cleaned_data['source_name']
            for name in source_names:
                name = name.strip()
                if name:
                    source, created = DrinkingWaterSystem.objects.get_or_create(name=name)
                    drinking_water.source_name.add(source)

            source_names = request.POST.getlist('other_sources')
            sources = request.POST.getlist('source')
            if source_names:
                for name in source_names:
                    source, created = DrinkingWaterSystem.objects.get_or_create(name=name.strip())
                    drinking_water.source_name.add(source)

            if sources:
                for name in sources:
                    water_source, created1 = DrinkingWaterSourceName.objects.get_or_create(name=name.strip()) 
                    drinking_water.source.add(water_source)                 

            messages.success(request, "Drinking water source data saved successfully!")
            return redirect("guestroom_consumption")
    else:
        if details:
            form = DrinkingWaterSourceForm(instance=details)
        else:
            form = DrinkingWaterSourceForm()

    drinking_object = DrinkingWaterSource.objects.filter(user=current_user).first()
    sources = []
    water_sources = []
    if drinking_object:
        sources = drinking_object.source_name.all() 
        water_sources = drinking_object.source.all()  

    return render(
        request, "DrinkingWaterSource.html", {"form": form, "details": details, 'sources': sources, 'water_sources': water_sources}
    )


@login_required
def delete_drinking_water_source(request):
    current_user = request.user
    DrinkingWaterSource.objects.filter(user=current_user).delete()
    return redirect("drinking_water_source")


@login_required
def restaurant_consumption_view(request):
    current_user = request.user
    details = RestaurantConsumption.objects.filter(user=current_user).first()
    all_details = RestaurantConsumption.objects.filter(user=current_user)
    if request.method == "POST":
        form = RestaurantConsumptionForm(request.POST)
        if form.is_valid():
            restaurant_consumption = form.save(commit=False)
            restaurant_consumption.user = current_user
            restaurant_consumption.save()
            messages.success(request, "Restaurant consumption data saved successfully!")
            return redirect("restaurant_consumption")
    else:
        form = RestaurantConsumptionForm()
    return render(
        request,
        "RestaurantConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
    )


@login_required
def delete_restaurant_consumption(request):
    current_user = request.user
    RestaurantConsumption.objects.filter(user=current_user).delete()
    return redirect("restaurant_consumption")


@login_required
def delete_restaurant(request, restaurant_id):
    # Get the restaurant object to delete
    restaurant = get_object_or_404(RestaurantConsumption, id=restaurant_id)
    # Delete the restaurant
    restaurant.delete()

    return redirect("restaurant_consumption")


@login_required
def banquet_consumption_view(request):
    current_user = request.user
    details = BanquetConsumption.objects.filter(user=current_user).first()
    all_details = BanquetConsumption.objects.filter(user=current_user)
    if request.method == "POST":
        form = BanquetConsumptionForm(request.POST)
        if form.is_valid():
            banquet_consumption = form.save(commit=False)
            banquet_consumption.user = current_user
            banquet_consumption.save()

            other_sources = form.cleaned_data['drinking_water_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = BanquetSource.objects.get_or_create(name=name)
                    banquet_consumption.drinking_water_source.add(source)

            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:
                    source, created = BanquetSource.objects.get_or_create(name=name.strip())
                    banquet_consumption.drinking_water_source.add(source)  

            messages.success(request, "Banquet consumption data saved successfully!")
            return redirect("banquet_consumption")
    else:
        form = BanquetConsumptionForm()

    banquet_object = BanquetConsumption.objects.filter(user=current_user).first()
    sources = []
    if banquet_object:
        sources = banquet_object.drinking_water_source.all()

    return render(
        request,
        "BanquetConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'sources': sources},
    )


@login_required
def delete_banquet_consumption(request):
    current_user = request.user
    BanquetConsumption.objects.filter(user=current_user).delete()
    return redirect("banquet_consumption")


@login_required
def delete_banquet(request, banquet_id):
    # Get the restaurant object to delete
    banquet = get_object_or_404(BanquetConsumption, id=banquet_id)
    # Delete the restaurant
    banquet.delete()

    return redirect("banquet_consumption")


@login_required
def guestroom_consumption_view(request):
    current_user = request.user
    details = GuestRoomConsumption.objects.filter(user=current_user).first()
    all_details = GuestRoomConsumption.objects.filter(user=current_user)
    if request.method == "POST":
        form = GuestRoomConsumptionForm(request.POST)
        if form.is_valid():
            guestroom_consumption = form.save(commit=False)
            guestroom_consumption.user = current_user
            guestroom_consumption.save()

            other_domestic_sources = form.cleaned_data['domestic_flushing_source']
            other_toilet_sources = form.cleaned_data['toilet_flushing_source']
            for name in other_domestic_sources:
                name = name.strip()
                if name:
                    domestic_source, created = GuestRoomDomesticSource.objects.get_or_create(name=name)
                    guestroom_consumption.domestic_flushing_source.add(domestic_source)

            for name in other_toilet_sources:
                name = name.strip()
                if name:
                    toilet_source, created = GuestRoomToiletSource.objects.get_or_create(name=name)
                    guestroom_consumption.toilet_flushing_source.add(toilet_source)   

            other_domestic_sources = request.POST.getlist('other_domestic_sources')
            other_toilet_sources = request.POST.getlist('other_toilet_sources')

            if other_domestic_sources:
                for name in other_domestic_sources:
                    domestic_source, created = GuestRoomDomesticSource.objects.get_or_create(name=name.strip())
                    guestroom_consumption.domestic_flushing_source.add(domestic_source) 

            if other_toilet_sources:
                for name in other_toilet_sources:
                    toilet_source, created = GuestRoomToiletSource.objects.get_or_create(name=name.strip())
                    guestroom_consumption.toilet_flushing_source.add(toilet_source)

            messages.success(request, "Guest Room consumption data saved successfully!")
            return redirect("guestroom_consumption")
    else:
        form = GuestRoomConsumptionForm()

    guestroom_object = GuestRoomConsumption.objects.filter(user=current_user).first()
    domestic_sources = []
    toilet_sources = []
    if guestroom_object:
        domestic_sources = guestroom_object.domestic_flushing_source.all()
        toilet_sources = guestroom_object.toilet_flushing_source.all()

    return render(
        request,
        "GuestRoomConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'domestic_sources': domestic_sources, 'toilet_sources': toilet_sources},
    )


@login_required
def delete_guestroom_consumption(request):
    current_user = request.user
    GuestRoomConsumption.objects.filter(user=current_user).delete()
    return redirect("guestroom_consumption")


@login_required
def delete_guestroom(request, guestroom_id):
    # Get the restaurant object to delete
    guestroom = get_object_or_404(GuestRoomConsumption, id=guestroom_id)
    # Delete the restaurant
    guestroom.delete()

    return redirect("guestroom_consumption")


@login_required
def employeeroom_consumption_view(request):
    current_user = request.user
    details = EmployeeRoomConsumption.objects.filter(user=current_user).first()
    all_details = EmployeeRoomConsumption.objects.filter(user=current_user)
    if request.method == "POST":
        form = EmployeeRoomConsumptionForm(request.POST)
        if form.is_valid():
            employeeroom_consumption = form.save(commit=False)
            employeeroom_consumption.user = current_user
            employeeroom_consumption.save()

            other_domestic_sources = form.cleaned_data['domestic_flushing_source']
            other_toilet_sources = form.cleaned_data['toilet_flushing_source']
            for name in other_domestic_sources:
                name = name.strip()
                if name:
                    domestic_source, created = EmployeeRoomDomesticSource.objects.get_or_create(name=name)
                    employeeroom_consumption.domestic_flushing_source.add(domestic_source)

            for name in other_toilet_sources:
                name = name.strip()
                if name:
                    toilet_source, created = EmployeeRoomToiletSource.objects.get_or_create(name=name)
                    employeeroom_consumption.toilet_flushing_source.add(toilet_source)   

            other_domestic_sources = request.POST.getlist('other_domestic_sources')
            other_toilet_sources = request.POST.getlist('other_toilet_sources')

            if other_domestic_sources:
                for name in other_domestic_sources:
                    domestic_source, created = EmployeeRoomDomesticSource.objects.get_or_create(name=name.strip())
                    employeeroom_consumption.domestic_flushing_source.add(domestic_source) 

            if other_toilet_sources:
                for name in other_toilet_sources:
                    toilet_source, created = EmployeeRoomToiletSource.objects.get_or_create(name=name.strip())
                    employeeroom_consumption.toilet_flushing_source.add(toilet_source)
                    
            return redirect("employeeroom_consumption")
    else:
        form = EmployeeRoomConsumptionForm()

    employeeroom_object = EmployeeRoomConsumption.objects.filter(user=current_user).first()
    domestic_sources = []
    toilet_sources = []
    if employeeroom_object:
        domestic_sources = employeeroom_object.domestic_flushing_source.all()
        toilet_sources = employeeroom_object.toilet_flushing_source.all()

    return render(
        request,
        "EmployeeRoomConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'domestic_sources': domestic_sources, 'toilet_sources': toilet_sources},
    )


@login_required
def delete_employeeroom_consumption(request):
    current_user = request.user
    EmployeeRoomConsumption.objects.filter(user=current_user).delete()
    return redirect("employeeroom_consumption")


@login_required
def delete_employeeroom(request, employeeroom_id):
    # Get the restaurant object to delete
    employeeroom = get_object_or_404(EmployeeRoomConsumption, id=employeeroom_id)
    # Delete the restaurant
    employeeroom.delete()

    return redirect("employeeroom_consumption")


@login_required
def driversroom_consumption_view(request):
    current_user = request.user
    details = DriversRoomConsumption.objects.filter(user=current_user).first()
    all_details = DriversRoomConsumption.objects.filter(user=current_user)
    if request.method == "POST":
        form = DriversRoomConsumptionForm(request.POST)
        if form.is_valid():
            driversroom_consumption = form.save(commit=False)
            driversroom_consumption.user = current_user
            driversroom_consumption.save()
            # if driversroom_consumption.other_source_name:
            #     driversroom_consumption.drivers_room_source = driversroom_consumption.other_source_name
            other_domestic_sources = form.cleaned_data['domestic_flushing_source']
            other_toilet_sources = form.cleaned_data['toilet_flushing_source']
            for name in other_domestic_sources:
                name = name.strip()
                if name:
                    domestic_source, created = DriversRoomDomesticSource.objects.get_or_create(name=name)
                    driversroom_consumption.domestic_flushing_source.add(domestic_source)

            for name in other_toilet_sources:
                name = name.strip()
                if name:
                    toilet_source, created = DriversRoomToiletSource.objects.get_or_create(name=name)
                    driversroom_consumption.toilet_flushing_source.add(toilet_source)   

            other_domestic_sources = request.POST.getlist('other_domestic_sources')
            other_toilet_sources = request.POST.getlist('other_toilet_sources')

            if other_domestic_sources:
                for name in other_domestic_sources:
                    domestic_source, created = DriversRoomDomesticSource.objects.get_or_create(name=name.strip())
                    driversroom_consumption.domestic_flushing_source.add(domestic_source) 

            if other_toilet_sources:
                for name in other_toilet_sources:
                    toilet_source, created = DriversRoomToiletSource.objects.get_or_create(name=name.strip())
                    driversroom_consumption.toilet_flushing_source.add(toilet_source)

            return redirect("driversroom_consumption")
    else:
        form = DriversRoomConsumptionForm()

    driversroom_object = DriversRoomConsumption.objects.filter(user=current_user).first()
    domestic_sources = []
    toilet_sources = []
    if driversroom_object:
        domestic_sources = driversroom_object.domestic_flushing_source.all()
        toilet_sources = driversroom_object.toilet_flushing_source.all()

    return render(
        request,
        "DriversRoomConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'domestic_sources': domestic_sources, 'toilet_sources': toilet_sources},
    )


@login_required
def delete_driversroom_consumption(request):
    current_user = request.user
    DriversRoomConsumption.objects.filter(user=current_user).delete()
    return redirect("driversroom_consumption")


@login_required
def delete_driversroom(request, driversroom_id):
    # Get the restaurant object to delete
    driversroom = get_object_or_404(DriversRoomConsumption, id=driversroom_id)
    # Delete the restaurant
    driversroom.delete()

    return redirect("driversroom_consumption")


@login_required
def swimmingpool_consumption_view(request):
    # sourcery skip: merge-else-if-into-elif, use-named-expression
    current_user = request.user
    details = SwimmingPoolConsumption.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = SwimmingPoolConsumptionForm(request.POST)
        if form.is_valid():
            swimmingpool_consumption = form.save(commit=False)
            swimmingpool_consumption.user = current_user
            swimmingpool_consumption.save()
            
            other_sources = form.cleaned_data['swimming_pool_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = SwimmingPoolSource.objects.get_or_create(name=name)
                    swimmingpool_consumption.swimming_pool_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = SwimmingPoolSource.objects.get_or_create(name=name.strip())
                    swimmingpool_consumption.swimming_pool_source.add(source)
                
            return redirect("waterbodies_consumption")
        else:
            print(form.errors)
    else:
        if details:
            form = SwimmingPoolConsumptionForm(instance=details)
        else:
            form = SwimmingPoolConsumptionForm()
            
    swimming_object = SwimmingPoolConsumption.objects.filter(user=current_user).first()
    sources = []
    if swimming_object:
        sources = swimming_object.swimming_pool_source.all()
    
    return render(
        request, "SwimmingPoolConsumption.html", {"form": form, "details": details, "sources": sources}
    )
# for source in SwimmingPoolConsumption.objects.all():
#     print(source.swimming_pool_source.all())


@login_required
def delete_swimmingpool_consumption(request):
    current_user = request.user
    SwimmingPoolConsumption.objects.filter(user=current_user).delete()
    return redirect("swimmingpool_consumption")


@login_required
def waterbodies_consumption_view(request):
    current_user = request.user
    details = WaterBodiesConsumption.objects.filter(user=current_user).first()
    print(details)
    if request.method == "POST":
        print('post')
        form = WaterBodiesConsumptionForm(request.POST)
        if form.is_valid():
            print('form')
            waterbody_consumption = form.save(commit=False)
            waterbody_consumption.user = current_user
            waterbody_consumption.save()

            other_sources = form.cleaned_data['water_body_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = WaterBodiesSource.objects.get_or_create(name=name)
                    waterbody_consumption.water_body_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = WaterBodiesSource.objects.get_or_create(name=name.strip())
                    waterbody_consumption.water_body_source.add(source)
            return redirect("laundry_consumption")
        else:
            print(form.errors)
    else:
        if details:
            form = WaterBodiesConsumptionForm(instance=details)
        else:
            form = WaterBodiesConsumptionForm()

    waterbody_object = WaterBodiesConsumption.objects.filter(user=current_user).first()
    sources = []
    if waterbody_object:
        sources = waterbody_object.water_body_source.all()

    return render(
        request, "WaterBodiesConsumption.html", {"form": form, "details": details, 'sources': sources}
    )


@login_required
def delete_waterbodies_consumption(request):
    current_user = request.user
    WaterBodiesConsumption.objects.filter(user=current_user).delete()
    return redirect('waterbodies_consumption')



@login_required
def source_dash_view(request):
    user_dash_app = create_user_dash_app(request.user)
    sources = SourceWaterProfile.objects.filter(user=request.user).all()
    return render(request, "DashSource.html")


def laundry_consumption_view(request):
    current_user = request.user
    details = LaundryConsumption.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = LaundryConsumptionForm(request.POST)
        if form.is_valid():
            laundry_consumption = form.save(commit=False)
            laundry_consumption.user = current_user
            laundry_consumption.save()

            other_sources = form.cleaned_data['laundry_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = LaundrySource.objects.get_or_create(name=name)
                    laundry_consumption.laundry_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = LaundrySource.objects.get_or_create(name=name.strip())
                    laundry_consumption.laundry_source.add(source)
            return redirect("boiler_consumption")
    else:
        if details:
            form = LaundryConsumptionForm(instance=details)
        else:
            form = LaundryConsumptionForm()

    laundry_object = LaundryConsumption.objects.filter(user=current_user).first()
    sources = []
    if laundry_object:
        sources = laundry_object.laundry_source.all()

    return render(
        request, "LaundryConsumption.html", {"form": form, "details": details, 'sources': sources}
    )


@login_required
def delete_laundry_consumption(request):
    current_user = request.user
    LaundryConsumption.objects.filter(user=current_user).delete()
    return redirect("laundry_consumption")


@login_required
def boiler_consumption_view(request):
    current_user = request.user
    consumption_details = BoilerConsumption.objects.filter(user=current_user).first()
    all_details = BoilerConsumption.objects.filter(user=current_user)
    all_treatment_methods = BoilerTreatmentMethods.objects.filter(user=request.user)

    if request.method == "POST":
        consumption_form = BoilerConsumptionForm(request.POST, prefix="consumption")

        if consumption_form.is_valid():
            consumption = consumption_form.save(commit=False)
            consumption.user = current_user
            consumption.save()

            other_sources = consumption_form.cleaned_data['boiler_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = BoilerSource.objects.get_or_create(name=name)
                    consumption.boiler_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = BoilerSource.objects.get_or_create(name=name.strip())
                    consumption.boiler_source.add(source)
                    
            pre_treatment = consumption_form.cleaned_data.get("pre_treatment_boiler")
            if pre_treatment == "2":
                return redirect("boiler_treatment_method")
            else:
                return redirect("add_boiler")
    else:
        if consumption_details:
            consumption_form = BoilerConsumptionForm(
                instance=consumption_details, prefix="consumption"
            )
        else:
            consumption_form = BoilerConsumptionForm(prefix="consumption")

    boiler_object = BoilerConsumption.objects.filter(user=current_user).first()
    sources = []
    if_steam = None
    if boiler_object:
        sources = boiler_object.boiler_source.all()        
        if_steam = boiler_object.steam_recovery

    return render(
        request,
        "BoilerConsumption.html",
        {
            "consumption_form": consumption_form,
            "details": consumption_details,
            "all_details": all_details,
            "all_treatment_methods": all_treatment_methods,
            "sources": sources,
            "if_steam" : if_steam
        },
    )


@login_required
def delete_boiler_consumption(request):
    current_user = request.user
    BoilerConsumption.objects.filter(user=current_user).delete()
    BoilerTreatmentMethods.objects.filter(user=current_user).delete()
    return redirect("boiler_consumption")


@login_required
def boiler_treatment_methods_view(request):
    current_user = request.user
    all_treatment_methods = BoilerTreatmentMethods.objects.filter(user=request.user)

    if request.method == "POST":
        treatment_form = BoilerTreatmentMethodsForm(request.POST, prefix="treatment")
        if treatment_form.is_valid():
            treatment = treatment_form.save(commit=False)
            treatment.user = current_user
            treatment.save()
            return redirect("boiler_treatment_method")
    else:
        treatment_form = BoilerTreatmentMethodsForm(prefix="treatment")

    return render(
        request,
        "BoilerTreatmentMethod.html",
        {
            "treatment_form": treatment_form,
            "all_treatment_methods": all_treatment_methods,
        },
    )


@login_required
def delete_boiler_treatment_method(request, boiler_treatment_id):
    # Get the restaurant object to delete
    boiler_treatment = get_object_or_404(BoilerTreatmentMethods, id=boiler_treatment_id)
    # Delete the restaurant
    boiler_treatment.delete()

    return redirect("boiler_treatment_method")


@login_required
def add_boiler_view(request):
    current_user = request.user
    details = AddBoilerConsumption.objects.filter(user=current_user).first()
    all_details = AddBoilerConsumption.objects.filter(user=current_user)
    all_treatment_methods = BoilerTreatmentMethods.objects.filter(user=request.user)

    if request.method == "POST":
        form = AddBoilerConsumptionForm(request.POST)
        if form.is_valid():
            add_boiler = form.save(commit=False)
            add_boiler.user = current_user
            add_boiler.save()
            return redirect("add_boiler")
    else:
        form = AddBoilerConsumptionForm()
    return render(
        request,
        "AddBoilerConsumption.html",
        {
            "form": form,
            "details": details,
            "all_details": all_details,
            "all_treatment_methods": all_treatment_methods,
        },
    )


@login_required
def delete_each_boiler_consumption(request):
    current_user = request.user
    AddBoilerConsumption.objects.filter(user=current_user).delete()
    return redirect("add_boiler")


@login_required
def delete_each_boiler(request, boiler_id):
    # Get the boiler object to delete
    boiler = get_object_or_404(AddBoilerConsumption, id=boiler_id)
    # Delete the boiler
    boiler.delete()

    return redirect("add_boiler")


@login_required
def calorifier_consumption_view(request):
    current_user = request.user
    details = CalorifierConsumption.objects.filter(user=current_user).first()
    all_details = CalorifierConsumption.objects.filter(user=current_user)

    if request.method == "POST":
        form = CalorifierConsumptionForm(request.POST)
        if form.is_valid():
            calorifier = form.save(commit=False)
            calorifier.user = current_user
            calorifier.save()

            other_sources = form.cleaned_data['calorifier_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = CalorifierSource.objects.get_or_create(name=name)
                    calorifier.calorifier_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = CalorifierSource.objects.get_or_create(name=name.strip())
                    calorifier.calorifier_source.add(source)
        
            return redirect("calorifier_consumption")
    else:
        form = CalorifierConsumptionForm()

    calorifier_object = CalorifierConsumption.objects.filter(user=current_user).first()
    sources = []
    if calorifier_object:
        sources = calorifier_object.calorifier_source.all()

    return render(
        request,
        "CalorifierConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'sources': sources},
    )


@login_required
def delete_calorifier_consumption(request):
    current_user = request.user
    CalorifierConsumption.objects.filter(user=current_user).delete()
    return redirect("calorifier_consumption")


@login_required
def delete_calorifier(request, calorifier_id):
    # Get the boiler object to delete
    calorifier = get_object_or_404(CalorifierConsumption, id=calorifier_id)
    # Delete the boiler
    calorifier.delete()

    return redirect("calorifier_consumption")


@login_required
def coolingtower_consumption_view(request):
    current_user = request.user
    details = CoolingTowerConsumption.objects.filter(user=current_user).first()
    all_details = CoolingTowerConsumption.objects.filter(user=current_user)

    if request.method == "POST":
        form = CoolingTowerConsumptionForm(request.POST)

        if form.is_valid():
            cooling_tower = form.save(commit=False)
            cooling_tower.user = current_user
            cooling_tower.save()
            return redirect("add_coolingtower")
    else:
        if details:
            form = CoolingTowerConsumptionForm(instance=details)
        else:
            form = CoolingTowerConsumptionForm()

    return render(
        request,
        "CoolingTowerConsumption.html",
        {"form": form, "details": details, "all_details": all_details},
    )


@login_required
def delete_coolingtower_consumption(request):
    current_user = request.user
    CoolingTowerConsumption.objects.filter(user=current_user).delete()
    return redirect("coolingtower_consumption")


@login_required
def add_coolingtower_view(request):
    current_user = request.user
    details = AddCoolingTowerConsumption.objects.filter(user=current_user).first()
    all_details = AddCoolingTowerConsumption.objects.filter(user=current_user)

    if request.method == "POST":
        form = AddCoolingTowerConsumptionForm(request.POST)
        if form.is_valid():
            add_coolingtower = form.save(commit=False)
            add_coolingtower.user = current_user
            add_coolingtower.save()

            other_sources = form.cleaned_data['cooling_tower_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = AddCoolingTowerSource.objects.get_or_create(name=name)
                    add_coolingtower.cooling_tower_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = AddCoolingTowerSource.objects.get_or_create(name=name.strip())
                    add_coolingtower.cooling_tower_source.add(source)

            return redirect("add_coolingtower")
    else:
        form = AddCoolingTowerConsumptionForm()

    addCoolingTower_object = AddCoolingTowerConsumption.objects.filter(user=current_user).first()
    sources = []
    if addCoolingTower_object:
        sources = addCoolingTower_object.cooling_tower_source.all()

    return render(
        request,
        "AddCoolingTowerConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'sources': sources},
    )


@login_required
def delete_each_coolingtower_consumption(request):
    current_user = request.user
    AddCoolingTowerConsumption.objects.filter(user=current_user).delete()
    return redirect("add_coolingtower")


@login_required
def delete_each_coolingtower(request, coolingtower_id):
    # Get the boiler object to delete
    coolingtower = get_object_or_404(AddCoolingTowerConsumption, id=coolingtower_id)
    # Delete the boiler
    coolingtower.delete()

    return redirect("add_coolingtower")


@login_required
def irrigation_consumption_view(request):
    current_user = request.user
    details = IrrigationConsumption.objects.filter(user=current_user).first()
    all_details = IrrigationConsumption.objects.filter(user=current_user)

    if request.method == "POST":
        form = IrrigationConsumptionForm(request.POST)

        if form.is_valid():
            irrigation = form.save(commit=False)
            irrigation.user = current_user
            irrigation.save()

            other_sources = form.cleaned_data['irrigation_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = IrrigationSource.objects.get_or_create(name=name)
                    irrigation.irrigation_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = IrrigationSource.objects.get_or_create(name=name.strip())
                    irrigation.irrigation_source.add(source)
            return redirect("other_consumption")
    else:
        if details:
            form = IrrigationConsumptionForm(instance=details)
        else:
            form = IrrigationConsumptionForm()

    irrigation_object = IrrigationConsumption.objects.filter(user=current_user).first()
    sources = []
    if irrigation_object:
        sources = irrigation_object.irrigation_source.all()        

    return render(
        request,
        "IrrigationConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'sources': sources},
    )


@login_required
def delete_irrigation_consumption(request):
    current_user = request.user
    IrrigationConsumption.objects.filter(user=current_user).delete()
    return redirect("irrigation_consumption")


@login_required
def other_consumption_view(request):
    current_user = request.user
    details = OtherConsumption.objects.filter(user=current_user).first()
    all_details = OtherConsumption.objects.filter(user=current_user)

    if request.method == "POST":
        form = OtherConsumptionForm(request.POST)

        if form.is_valid():
            other_consumption = form.save(commit=False)
            other_consumption.user = current_user
            other_consumption.save()

            other_sources = form.cleaned_data['other_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = OtherConsumptionSource.objects.get_or_create(name=name)
                    other_consumption.other_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = OtherConsumptionSource.objects.get_or_create(name=name.strip())
                    other_consumption.other_source.add(source)
            return redirect("wastewater_treatment")
    else:
        if details:
            form = OtherConsumptionForm(instance=details)
        else:
            form = OtherConsumptionForm()

    other_consumption_object = OtherConsumption.objects.filter(user=current_user).first()
    sources = []
    if other_consumption_object:
        sources = other_consumption_object.other_source.all()        

    return render(
        request,
        "OtherConsumption.html",
        {"form": form, "details": details, "all_details": all_details, 'sources': sources},
    )


@login_required
def delete_other_consumption(request):
    current_user = request.user
    OtherConsumption.objects.filter(user=current_user).delete()
    return redirect("other_consumption")


@login_required
def wastewater_treatment_view(request):
    current_user = request.user
    details = WasteWaterTreatment.objects.filter(user=current_user).first()
    # details1 = WasteWaterTreatmentSTP.objects.filter(user=current_user).first()
    # details2 = WasteWaterTreatmentETP.objects.filter(user=current_user).first()
    # details3 = WasteWaterTreatmentOthers.objects.filter(user=current_user).first()

    if request.method == "POST":
        form = WasteWaterTreatmentForm(request.POST)

        if form.is_valid():
            waste_water = form.save(commit=False)
            waste_water.user = current_user
            waste_water.save()
            if form.cleaned_data.get("treatment_method") == "STP":
                return redirect("wastewater_treatment_STP")
            elif form.cleaned_data.get("treatment_method") == "ETP":
                return redirect("wastewater_treatment_ETP")
            else:
                return redirect("wastewater_treatment_Others")
    else:
        if details:
            form = WasteWaterTreatmentForm(instance=details)
        else:
            form = WasteWaterTreatmentForm()

    return render(
        request, "WasteWaterTreatment.html", {"form": form, "details": details}
    )


@login_required
def delete_wastewater_treatment(request):
    current_user = request.user
    WasteWaterTreatment.objects.filter(user=current_user).delete()
    WasteWaterTreatmentSTP.objects.filter(user=current_user).delete()
    WasteWaterTreatmentETP.objects.filter(user=current_user).delete()
    WasteWaterTreatmentOthers.objects.filter(user=current_user).delete()
    return redirect("wastewater_treatment")


@login_required
def wastewater_treatment_STP_view(request):
    current_user = request.user
    details = WasteWaterTreatmentSTP.objects.filter(user=current_user).first()

    if request.method == "POST":
        form = WasteWaterTreatmentSTPForm(request.POST)

        if form.is_valid():
            wastewater_treatment_STP = form.save(commit=False)
            wastewater_treatment_STP.user = current_user
            wastewater_treatment_STP.save()
            return redirect("tanks_and_capacities")
    else:
        if details:
            form = WasteWaterTreatmentSTPForm(instance=details)
        else:
            form = WasteWaterTreatmentSTPForm()

    return render(
        request, "WasteWaterTreatmentSTP.html", {"form": form, "details": details}
    )


@login_required
def delete_wastewater_treatment_STP(request):
    current_user = request.user
    WasteWaterTreatmentSTP.objects.filter(user=current_user).delete()
    return redirect("wastewater_treatment_STP")


@login_required
def wastewater_treatment_ETP_view(request):
    current_user = request.user
    details = WasteWaterTreatmentETP.objects.filter(user=current_user).first()

    if request.method == "POST":
        form = WasteWaterTreatmentETPForm(request.POST)

        if form.is_valid():
            wastewater_treatment_ETP = form.save(commit=False)
            wastewater_treatment_ETP.user = current_user
            wastewater_treatment_ETP.save()
            return redirect("tanks_and_capacities")
    else:
        if details:
            form = WasteWaterTreatmentETPForm(instance=details)
        else:
            form = WasteWaterTreatmentETPForm()

    return render(
        request, "WasteWaterTreatmentETP.html", {"form": form, "details": details}
    )


@login_required
def delete_wastewater_treatment_ETP(request):
    current_user = request.user
    WasteWaterTreatmentETP.objects.filter(user=current_user).delete()
    return redirect("wastewater_treatment_ETP")


@login_required
def wastewater_treatment_Others_view(request):
    current_user = request.user
    details = WasteWaterTreatmentOthers.objects.filter(user=current_user).first()

    if request.method == "POST":
        form = WasteWaterTreatmentOthersForm(request.POST)

        if form.is_valid():
            wastewater_treatment_Others = form.save(commit=False)
            wastewater_treatment_Others.user = current_user
            wastewater_treatment_Others.save()
            return redirect("tanks_and_capacities")
    else:
        if details:
            form = WasteWaterTreatmentOthersForm(instance=details)
        else:
            form = WasteWaterTreatmentOthersForm()

    return render(
        request, "WasteWaterTreatmentOthers.html", {"form": form, "details": details}
    )


@login_required
def delete_wastewater_treatment_Others(request):
    current_user = request.user
    WasteWaterTreatmentETP.objects.filter(user=current_user).delete()
    return redirect("wastewater_treatment_Others")


@login_required
def tanks_and_capacities_view(request):
    current_user = request.user
    details = TanksAndCapacities.objects.filter(user=current_user).first()
    water_treatment_details = WasteWaterTreatment.objects.filter(
        user=current_user
    ).first()
    print(water_treatment_details)

    if request.method == "POST":
        form = TanksAndCapacitiesForm(request.POST)

        if form.is_valid():
            tanks_and_capacities = form.save(commit=False)
            tanks_and_capacities.user = current_user
            tanks_and_capacities.save()

            other_sources = form.cleaned_data['tank_source']
            for name in other_sources:
                name = name.strip()
                if name:
                    source, created = TanksAndCapacitiesSource.objects.get_or_create(name=name)
                    tanks_and_capacities.tank_source.add(source)
            
            other_sources = request.POST.getlist('other_sources')
            if other_sources:
                for name in other_sources:  # Assuming comma-separated names
                    source, created = SwimmingPoolSource.objects.get_or_create(name=name.strip())
                    tanks_and_capacities.tank_source.add(source)
            return redirect("water_quality_profile")
    else:
        if details:
            form = TanksAndCapacitiesForm(instance=details)
        else:
            form = TanksAndCapacitiesForm()

    tanksandcapacities_object = TanksAndCapacities.objects.filter(user=current_user).first()
    sources = []
    if tanksandcapacities_object:
        sources = tanksandcapacities_object.tank_source.all()
            

    return render(
        request,
        "TanksAndCapacities.html",
        {
            "form": form,
            "details": details,
            "water_treatment_details": water_treatment_details,
            "sources": sources
        },
    )


@login_required
def delete_tanks_and_capacities(request):
    current_user = request.user
    TanksAndCapacities.objects.filter(user=current_user).delete()
    return redirect("tanks_and_capacities")


@login_required
def water_quality_profile_view(request):
    current_user = request.user
    details = WaterQualityProfile.objects.filter(user=current_user).first()
    water_treatment_details = WasteWaterTreatment.objects.filter(
        user=current_user
    ).first()

    if request.method == "POST":
        form = WaterQualityProfileForm(request.POST)

        if form.is_valid():
            water_quality_profile = form.save(commit=False)
            water_quality_profile.user = current_user
            water_quality_profile.save()
            return redirect("thank_you")
    else:
        if details:
            form = WaterQualityProfileForm(instance=details)
        else:
            form = WaterQualityProfileForm()

    return render(
        request, 
        "WaterQualityProfile.html", 
        {"form": form, 
         "details": details,
         "water_treatment_details": water_treatment_details,
        },
    )


@login_required
def delete_water_quality_profile(request):
    current_user = request.user
    WaterQualityProfile.objects.filter(user=current_user).delete()
    return redirect("water_quality_profile")


@login_required
def recycled_water_view(request):
    current_user = request.user
    all_details = RecycledWaterProfile.objects.filter(user=current_user)
    details = RecycledWaterProfile.objects.filter(user=current_user).first()
    if request.method == "POST":
        form = RecycledWaterProfileForm(request.POST)
        if form.is_valid():
            recycled_water = form.save(commit=False)
            recycled_water.user = request.user
            recycled_water.save()
            return redirect("recycled_water")
    else:
        form = RecycledWaterProfileForm()
    return render(
        request,
        "RecycledWater.html",
        {"form": form, "details": details, "all_details": all_details},
    )


@login_required
def delete_recycled_water_all(request):
    current_user = request.user
    RecycledWaterProfile.objects.filter(user=current_user).delete()
    return redirect("kitchen_consumption")


@login_required
def delete_recycled_water(request, recycled_water_id):
    # Get the restaurant object to delete
    recycled_water = get_object_or_404(RecycledWaterProfile, id=recycled_water_id)
    # Delete the restaurant
    recycled_water.delete()

    return redirect("recycled_water")


def show_map_view(request):
    return render(request, "rainfall_map.html")


def generate_pdf_file():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    doc.onFirstPage = lambda canvas, doc: canvas.setTitle("Digital Water Audit Report")

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = styles['Title'].clone('TitleStyle')
    title_style.textColor = colors.darkblue
    title_style.spaceAfter = 50
    title_style.fontSize = 28

    heading_style = styles['Heading1'].clone('HeadingStyle')
    heading_style.spaceBefore = 10
    heading_style.spaceAfter = 10
    heading_style.leftIndent = 20


    center_style = ParagraphStyle(name='Center', alignment=TA_CENTER)

    # Title
    elements = [Paragraph("Digital Water Audit Report", title_style)]

    # Logo image
    logo = "static/main_logo.png" 
    logo_img = Image(logo)  # Set width and height as needed
    logo_img.hAlign = 'CENTER'  
    elements.append(logo_img)
    elements.append(Spacer(1, 24))

    # Description Text
    description_text = "This report provides an detailed analysis of the water audit findings and insights."
    elements.append(Paragraph(description_text, center_style))
    
    elements.append(PageBreak())
    
    # Index Page
    
    elements.append(Paragraph("Index", title_style))
    elements.append(Spacer(1, 24))
    
    

    # List of sections
    sections = [
        "1. Introduction",
        "2. Source Water Profile",
        "3. Fresh Water Treatment Profile",
        "4. Tanks and Capacities",
        "5. Consumption Details",
        "6. Waste Water Treatment",
        "7. Water Quality Profile",
        "8. Recycled Water Profile",
        "9. Conclusion"
    ]

    for section in sections:
        elements.append(Paragraph(section, heading_style))

    doc.build(elements)

    buffer.seek(0)
    return buffer

@login_required
def generate_pdf(request):
    pdf_content = generate_pdf_file()
    response = FileResponse(pdf_content, filename='report.pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    return response