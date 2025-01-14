import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.graph_objects as go
import os

# Step 1: Get total land area and input dimensions for each room
def get_room_dimensions():
    total_area = float(input("Enter total land area in square feet: "))
    floors = int(input("Enter the number of floors: "))
    
    floor_areas = []
    for i in range(floors):
        print(f"\nEnter room dimensions for Floor {i + 1}:")
        floor_total_area = total_area
        
        bedroom_area = float(input(f"  Enter bedroom area in square feet (Remaining: {floor_total_area}): "))
        floor_total_area -= bedroom_area
        
        kitchen_area = float(input(f"  Enter kitchen area in square feet (Remaining: {floor_total_area}): "))
        floor_total_area -= kitchen_area
        
        livingroom_area = float(input(f"  Enter living room area in square feet (Remaining: {floor_total_area}): "))
        floor_total_area -= livingroom_area
        
        bathroom_area = float(input(f"  Enter bathroom area in square feet (Remaining: {floor_total_area}): "))
        floor_total_area -= bathroom_area
        
        if floor_total_area < 0:
            raise ValueError("The total area of the rooms exceeds the land area on this floor!")
        
        # Assume some aspect ratios for simplicity (length to width ratio)
        floor_areas.append({
            'bedroom': (bedroom_area ** 0.5, bedroom_area ** 0.5),  # Square shape
            'kitchen': (kitchen_area ** 0.5, kitchen_area ** 0.5),
            'livingroom': (livingroom_area ** 0.5, livingroom_area ** 0.5),
            'bathroom': (bathroom_area ** 0.5, bathroom_area ** 0.5)
        })
    
    return floor_areas, floors

# Step 2: Draw 3D blueprint for each floor
def draw_3d_blueprint(dimensions, floors):
    fig = go.Figure()

    wall_height = 10  # height for each floor's walls
    floor_color = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow']

    for floor in range(floors):
        z_offset = floor * wall_height  # Position each floor on top of the previous one
        
        # Bedroom
        fig.add_trace(go.Mesh3d(
            x=[0, dimensions[floor]['bedroom'][0], dimensions[floor]['bedroom'][0], 0],
            y=[0, 0, dimensions[floor]['bedroom'][1], dimensions[floor]['bedroom'][1]],
            z=[z_offset, z_offset, z_offset, z_offset],
            color=floor_color[0],
            name=f'Bedroom (Floor {floor + 1})',
            hoverinfo='text',
            hovertext=f'Bedroom (Floor {floor + 1})<br>{dimensions[floor]["bedroom"][0]*dimensions[floor]["bedroom"][1]} sq ft'
        ))

        # Kitchen next to the Bedroom
        kitchen_x = dimensions[floor]['bedroom'][0]
        fig.add_trace(go.Mesh3d(
            x=[kitchen_x, kitchen_x + dimensions[floor]['kitchen'][0], kitchen_x + dimensions[floor]['kitchen'][0], kitchen_x],
            y=[0, 0, dimensions[floor]['kitchen'][1], dimensions[floor]['kitchen'][1]],
            z=[z_offset, z_offset, z_offset, z_offset],
            color=floor_color[1],
            name=f'Kitchen (Floor {floor + 1})',
            hoverinfo='text',
            hovertext=f'Kitchen (Floor {floor + 1})<br>{dimensions[floor]["kitchen"][0]*dimensions[floor]["kitchen"][1]} sq ft'
        ))

        # Living Room
        livingroom_y = -dimensions[floor]['livingroom'][1]
        fig.add_trace(go.Mesh3d(
            x=[0, dimensions[floor]['livingroom'][0], dimensions[floor]['livingroom'][0], 0],
            y=[livingroom_y, livingroom_y, livingroom_y + dimensions[floor]['livingroom'][1], livingroom_y + dimensions[floor]['livingroom'][1]],
            z=[z_offset, z_offset, z_offset, z_offset],
            color=floor_color[2],
            name=f'Living Room (Floor {floor + 1})',
            hoverinfo='text',
            hovertext=f'Living Room (Floor {floor + 1})<br>{dimensions[floor]["livingroom"][0]*dimensions[floor]["livingroom"][1]} sq ft'
        ))

        # Bathroom
        bathroom_x = dimensions[floor]['livingroom'][0]
        bathroom_y = livingroom_y
        fig.add_trace(go.Mesh3d(
            x=[bathroom_x, bathroom_x + dimensions[floor]['bathroom'][0], bathroom_x + dimensions[floor]['bathroom'][0], bathroom_x],
            y=[bathroom_y, bathroom_y, bathroom_y + dimensions[floor]['bathroom'][1], bathroom_y + dimensions[floor]['bathroom'][1]],
            z=[z_offset, z_offset, z_offset, z_offset],
            color=floor_color[3],
            name=f'Bathroom (Floor {floor + 1})',
            hoverinfo='text',
            hovertext=f'Bathroom (Floor {floor + 1})<br>{dimensions[floor]["bathroom"][0]*dimensions[floor]["bathroom"][1]} sq ft'
        ))
    
    # Set up layout of the 3D plot
    fig.update_layout(
        title="3D House Blueprint with Multiple Floors",
        scene=dict(
            xaxis=dict(title='Length (ft)'),
            yaxis=dict(title='Width (ft)'),
            zaxis=dict(title='Height (ft)')
        )
    )
    
    fig.show()

# Step 3: Show 2D blueprint with room labels for each floor
def draw_2d_blueprint(dimensions, floors):
    fig, ax = plt.subplots()
    room_colors = {
        'Bedroom': 'lightblue',
        'Kitchen': 'lightgreen',
        'Living Room': 'lightyellow',
        'Bathroom': 'lightpink'
    }

    logos = ["C:/Users/sharp/OneDrive/Desktop/bedroom.jpg", "C:/Users/sharp/OneDrive/Desktop/kitchen.jpg", "C:/Users/sharp/OneDrive/Desktop/livingroom.jpg", "C:/Users/sharp/OneDrive/Desktop/bathroom.jpg"]

    for floor in range(floors):
        # Position variables for proper placement
        current_x = 0
        current_y = 0
        
        # Draw rooms with correct positioning
        ax.add_patch(patches.Rectangle((current_x, current_y), dimensions[floor]['bedroom'][0], dimensions[floor]['bedroom'][1],
                                        color=room_colors['Bedroom'], label=f'Bedroom (Floor {floor + 1})'))
        current_x += dimensions[floor]['bedroom'][0]  # Move x position for next room
        
        ax.add_patch(patches.Rectangle((current_x, current_y), dimensions[floor]['kitchen'][0], dimensions[floor]['kitchen'][1],
                                        color=room_colors['Kitchen'], label=f'Kitchen (Floor {floor + 1})'))
        current_x += dimensions[floor]['kitchen'][0]  # Move x position for next room
        
        ax.add_patch(patches.Rectangle((current_x, current_y), dimensions[floor]['livingroom'][0], dimensions[floor]['livingroom'][1],
                                        color=room_colors['Living Room'], label=f'Living Room (Floor {floor + 1})'))
        current_x += dimensions[floor]['livingroom'][0]  # Move x position for next room
        
        ax.add_patch(patches.Rectangle((current_x, current_y), dimensions[floor]['bathroom'][0], dimensions[floor]['bathroom'][1],
                                        color=room_colors['Bathroom'], label=f'Bathroom (Floor {floor + 1})'))
        
        # Logos Positioning
        positions = [
            (0 + dimensions[floor]['bedroom'][0] / 2, dimensions[floor]['bedroom'][1] + 0.5),
            (dimensions[floor]['bedroom'][0] + dimensions[floor]['kitchen'][0] / 2, dimensions[floor]['kitchen'][1] + 0.5),
            (dimensions[floor]['bedroom'][0] + dimensions[floor]['kitchen'][0] + dimensions[floor]['livingroom'][0] / 2, dimensions[floor]['livingroom'][1] + 0.5),
            (dimensions[floor]['bedroom'][0] + dimensions[floor]['kitchen'][0] + dimensions[floor]['livingroom'][0] + dimensions[floor]['bathroom'][0] / 2, dimensions[floor]['bathroom'][1] + 0.5)
        ]

        for pos, logo in zip(positions, logos):
            if os.path.exists(logo):
                img = plt.imread(logo)
                ax.imshow(img, extent=(pos[0]-0.5, pos[0]+0.5, pos[1]-0.5, pos[1]+0.5), aspect='auto')

    ax.set_xlim(0, sum(dim[0] for dim in dimensions[0].values()) + 10)
    ax.set_ylim(0, max(dim[1] for dim in dimensions[0].values()) + 10)
    ax.set_title("2D House Blueprint")
    ax.set_xlabel("Width (ft)")
    ax.set_ylabel("Length (ft)")
    ax.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    try:
        room_dimensions, num_floors = get_room_dimensions()
        draw_3d_blueprint(room_dimensions, num_floors)
        draw_2d_blueprint(room_dimensions, num_floors)
    except ValueError as e:
        print(e)
