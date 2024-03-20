from django.contrib import admin
from .models import Registration, BasicDetails, SourceWaterProfile, RainWaterProfile, FreshWaterTreatmentProfile, FreshWaterTreatmentProfileDetails, KitchenDishwasherTapConsumption,  DrinkingWaterSource, RestaurantConsumption, BanquetConsumption, GuestRoomConsumption, EmployeeRoomConsumption, DriversRoomConsumption, SwimmingPoolConsumption, WaterBodiesConsumption, LaundryConsumption, BoilerConsumption, BoilerTreatmentMethods, AddBoilerConsumption, CalorifierConsumption, CoolingTowerConsumption, AddCoolingTowerConsumption, IrrigationConsumption, OtherConsumption, WasteWaterTreatment, WasteWaterTreatmentETP, WasteWaterTreatmentOthers, WasteWaterTreatmentSTP, TanksAndCapacities, WaterQualityProfile, RecycledWaterProfile


admin.site.register(Registration)
admin.site.register(BasicDetails)
admin.site.register(SourceWaterProfile)
admin.site.register(FreshWaterTreatmentProfile)
admin.site.register(FreshWaterTreatmentProfileDetails)
admin.site.register(RainWaterProfile)
admin.site.register(KitchenDishwasherTapConsumption)
admin.site.register(DrinkingWaterSource)
admin.site.register(RestaurantConsumption)
admin.site.register(BanquetConsumption)
admin.site.register(GuestRoomConsumption)
admin.site.register(EmployeeRoomConsumption)
admin.site.register(DriversRoomConsumption)
admin.site.register(SwimmingPoolConsumption)
admin.site.register(WaterBodiesConsumption)
admin.site.register(LaundryConsumption)
admin.site.register(BoilerConsumption)
admin.site.register(BoilerTreatmentMethods)
admin.site.register(AddBoilerConsumption)
admin.site.register(CalorifierConsumption)
admin.site.register(CoolingTowerConsumption)
admin.site.register(AddCoolingTowerConsumption)
admin.site.register(IrrigationConsumption)
admin.site.register(OtherConsumption)
admin.site.register(WasteWaterTreatment)
admin.site.register(WasteWaterTreatmentSTP)
admin.site.register(WasteWaterTreatmentETP)
admin.site.register(WasteWaterTreatmentOthers)
admin.site.register(TanksAndCapacities)
admin.site.register(WaterQualityProfile)
admin.site.register(RecycledWaterProfile)