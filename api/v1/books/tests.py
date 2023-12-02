import os
import leafmap

os.environ["GOOGLE_API_KEY"] = "AIzaSyBgadQyILCS0Bn8WbB1N_qUFEbjQnj6-MI"
out_dir = os.path.expanduser(".")
lat = 50.97579908646006
lon = 11.023334842349778
radiusMeters = 50
view = "FULL_LAYERS"
requiredQuality = "HIGH"
pixelSizeMeters = 0.1
files = leafmap.get_solar_data(
    lat,
    lon,
    radiusMeters,
    view,
    requiredQuality,
    pixelSizeMeters,
    out_dir=out_dir
)
files
m = leafmap.Map()
m.add_raster(files['rgb'], layer_name="RGB")
m.add_raster(files['mask'], layer_name="Mask")
m.add_raster(files['dsm'], cmap='terrain', layer_name="DSM", visible=False)
m.add_raster(files['annualFlux'], cmap='plasma', layer_name="annualFlux")
m.add_raster(files['monthlyFlux'], cmap='plasma', band=[7], layer_name="monthlyFlux", visible=False)

m.add_colormap(cmap='terrain', vmin=190, vmax=250, label='Elevation (m)')
m.add_colormap(cmap='plasma', vmin=500, vmax=1000, label='Annual flux (kWh/kW/year)')
m
