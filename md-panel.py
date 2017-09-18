bl_info = {
	"name": "Panel para MD",
	"author": "Mario Mey",
	"version": (1, 0),
	"blender": (2, 6, 0),
	'location': '',
	"description": "Crea un panel para esconder DUMMIES, EMPTIES, camaras, luces, etc...",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "3D View"}


import bpy
#from bpy.props import *


class esconde():

	def esconde(self, que, bool):
		for objeto in bpy.data.objects:
			if objeto.name.startswith(que):
				#print(objeto.name)
				objeto.hide = bool

	def escondein(self, que, bool):
		for objeto in bpy.data.objects:
			if que in objeto.name:
				#print(objeto.name)
				objeto.hide = bool

esconde = esconde()

# GUI (Panel)
#
class VIEW3D_PT_escondedor(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'MD'

	# draw the gui
	def draw(self, context):

		layout = self.layout
		toolsettings = context.tool_settings

		col = layout.column(align=True)
		row = col.row(align=True)

		row.prop(toolsettings, "use_keyframe_insert_auto", text="", toggle=True)

		col = layout.column(align=True)
		row = col.row(align=True)
		col.operator('layers.on')
		
		row = col.row(align=True)
		col.operator('layer.md')

		col = layout.column(align=True)

		row = col.row(align=True)
		row.operator('init.actions')
		row.operator('reset.actions')

		col = layout.column(align=True)

		row = col.row(align=True)
		row.operator('hide.cam')
		row.operator('unhide.cam')

		row = col.row(align=True)
		row.operator('hide.luces')
		row.operator('unhide.luces')

		row = col.row(align=True)
		row.operator('hide.env')
		row.operator('unhide.env')

		row = col.row(align=True)
		row.operator('hide.empties')
		row.operator('unhide.empties')

		row = col.row()

		col = layout.column(align=True)
		col.operator('copy.action_md_to_box_camluces')

		row = col.row()
		col = layout.column(align=True)
		col.operator('selectable.meshes')

		#row = col.row()
		#row.operator('hide.escenario_hided')
		#row.operator('hide.escenario_unhided')

		#col = layout.column(align=True)
		#col.label(text="Dummies:")

		#row = col.row()
		#row.operator('hide.dummies_hided')
		#row.operator('hide.dummies_unhided')


class ACTIONMDTOBOX_OT_actionmdtobox(bpy.types.Operator):
	bl_label = 'ActionMD2Box-CamLuces'
	bl_idname = 'copy.action_md_to_box_camluces'
	bl_description = 'Copia el action de MD a BOX y a CamLuces'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		# Elije la BOX como objeto, por el nombre del seleccionado
		box_obj = bpy.data.objects[bpy.context.object.name.split('.')[0] + '.box']
		# Elije la CamLuces
		camluces_obj = bpy.data.objects['arm.camluces']

		# Separa el nombre del Action del seleccionado
		action_list = bpy.context.object.animation_data.action.name.split('.')

		# Crea nombre del Action nuevo para BOX
		action_nuevo_box = action_list[0] + '.box.' + action_list[2]
		# Crea nombre del Action nuevo para CamLuces
		action_nuevo_camluces = action_list[0] + '.camluces.' + action_list[2]

		# Asigna el Action a BOX
		try: 
			box_obj.animation_data.action = bpy.data.actions[action_nuevo_box]
		except:
			print('No existe Action:', action_nuevo_box, '=> Reset')
			action_nuevo_box = action_list[0] + '.box.reset'
			box_obj.animation_data.action = bpy.data.actions[action_nuevo_box]

		# Asigna el Action a CamLuces
		try:
			camluces_obj.animation_data.action = bpy.data.actions[action_nuevo_camluces]
		except:
			print('No existe Action:', action_nuevo_camluces, '=> Reset')
			action_nuevo_camluces = action_list[0] + '.camluces.reset'
			camluces_obj.animation_data.action = bpy.data.actions[action_nuevo_camluces]

		return {'FINISHED'}

class SELECTABLEMESH_OT_selectablemesh(bpy.types.Operator):
	bl_label = 'Selectable Mesh'
	bl_idname = 'selectable.meshes'
	bl_description = 'Hace selectable los meshes'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		# Elije la BOX como objeto, por el nombre del seleccionado
		if bpy.context.scene['selectable_mesh']:
			for obj in bpy.context.scene.objects:
				if 'mesh.' in obj.name:
					obj.hide_select = True
			bpy.context.scene['selectable_mesh'] = 0
			print('Objetos Mesh no seleccionables')
		
		else:
			for obj in bpy.context.scene.objects:
				if 'mesh.' in obj.name:
					obj.hide_select = False
			bpy.context.scene['selectable_mesh'] = 1
			print('Objetos Mesh seleccionables')
			
		return {'FINISHED'}

class LAYERSON_OT_layers_on(bpy.types.Operator):
	bl_label = 'Layers on/off'
	bl_idname = 'layers.on'
	bl_description = 'Activa layers necesarios'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		capas_visibles = [0, 1, 10, 11]
		
		for i in range(20):
			if i in capas_visibles:
				bpy.context.scene.layers[i] = True
				#~ print(i)
			else:
				bpy.context.scene.layers[i] = False
		
		return {'FINISHED'}

class LAYERSMD_OT_layer_md(bpy.types.Operator):
	bl_label = 'Layer-MD'
	bl_idname = 'layer.md'
	bl_description = 'Activa layer de MD'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		capas_visibles = [0]
		
		for i in range(20):
			if i in capas_visibles:
				bpy.context.scene.layers[i] = True
			else:
				bpy.context.scene.layers[i] = False

		return {'FINISHED'}

class RESET_OT_actions(bpy.types.Operator):
	bl_label = 'Reset Actions'
	bl_idname = 'reset.actions'
	bl_description = 'Reset actions a arm., camluces. y md-bounds.'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		bpy.context.scene.frame_current = 0
		#bpy.ops.object.mode_set(mode='OBJECT')
		for objeto in bpy.data.objects:
			if objeto.name.endswith('.arm'):
				prefijo = objeto.name.split('.')[0]
				objeto.animation_data.action = bpy.data.actions[prefijo + '.td.reset']
				print('Reset:', objeto.name)

			if objeto.name.endswith('.box'):
				prefijo = objeto.name.split('.')[0]
				objeto.animation_data.action = bpy.data.actions[prefijo + '.box.reset']
				print('Reset:', objeto.name)
				
				# Camluces, aca porque usa el prefijo
				bpy.data.objects['arm.camluces'].animation_data.action = bpy.data.actions[prefijo + '.camluces.reset']
				print('Reset: arm.camluces')

		return {'FINISHED'}

class INIT_OT_actions(bpy.types.Operator):
	bl_label = 'Init Actions'
	bl_idname = 'init.actions'
	bl_description = 'Actions iniciales a md, camluces y box'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	

	def execute(op, context):
		bpy.context.scene.frame_current = 0
		bpy.ops.object.mode_set(mode='OBJECT')
		objeto_previo = bpy.context.scene.objects.active
		bpy.context.scene.objects.active = bpy.data.objects["cam.frente"]
		bpy.ops.view3d.object_as_camera()
		
		for objeto in bpy.data.objects:
			if objeto.name.endswith('.arm'):
				prefijo = objeto.name.split('.')[0]
				objeto.animation_data.action = bpy.data.actions[prefijo + '.td.init']

			if objeto.name.endswith('.box'):
				prefijo = objeto.name.split('.')[0]
				objeto.animation_data.action = bpy.data.actions[prefijo + '.box.init']
	
				# Camluces, aca porque usa el prefijo
                # No se por que usaba .camluces.reposo y depsues le doy .camluces.init
				#if prefijo + '.camluces.reposo' in bpy.data.actions:
				bpy.data.objects['arm.camluces'].animation_data.action = bpy.data.actions[prefijo + '.camluces.init']

		return {'FINISHED'}

class HIDE_OT_hide_empties(bpy.types.Operator):
	bl_label = 'H Empt-Vid'
	bl_idname = 'hide.empties'
	bl_description = 'Esconde los empties'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		esconde.esconde('empty.', True)
		esconde.esconde('logic.', True)
		esconde.esconde('video.', True)
		return {'FINISHED'}

class HIDE_OT_unhide_empties(bpy.types.Operator):
	bl_label = 'UH Empt-Vid'
	bl_idname = 'unhide.empties'
	bl_description = 'Muestra los empties'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		esconde.esconde('empty.', False)
		esconde.esconde('logic.', False)
		esconde.esconde('video.', False)
		return {'FINISHED'}

class HIDE_OT_hide_env(bpy.types.Operator):
	bl_label = 'H Environment'
	bl_idname = 'hide.env'
	bl_description = 'Esconde enviroment'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		esconde.escondein('env', True)
		return {'FINISHED'}

class HIDE_OT_unhide_env(bpy.types.Operator):
	bl_label = 'UH Environment'
	bl_idname = 'unhide.env'
	bl_description = 'Muestra enviroment'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		esconde.escondein('env', False)
		return {'FINISHED'}

class HIDE_OT_hide_cam(bpy.types.Operator):
	bl_label = 'H cam/arm'
	bl_idname = 'hide.cam'
	bl_description = 'Esconde las cam'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		esconde.esconde('cam.', True)
		try:
			bpy.data.objects['arm.camluces'].hide = True
		except:
			pass

		return {'FINISHED'}

class HIDE_OT_unhide_cam(bpy.types.Operator):
	bl_label = 'UH cam/arm'
	bl_idname = 'unhide.cam'
	bl_description = 'Muestra las cam'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		esconde.esconde('cam.', False)
		try:
			bpy.data.objects['arm.camluces'].hide = False
		except:
			pass
			#raise

		return {'FINISHED'}

class HIDE_OT_hide_luces(bpy.types.Operator):
	bl_label = 'H luces'
	bl_idname = 'hide.luces'
	bl_description = 'Esconde las luces'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		esconde.esconde('luz.', True)

		return {'FINISHED'}

class HIDE_OT_unhide_luces(bpy.types.Operator):
	bl_label = 'UH luces'
	bl_idname = 'unhide.luces'
	bl_description = 'Muestra las luces'
	bl_options = {'REGISTER', 'UNDO'}
	
	# on mouse up:
	def invoke(self, context, event):
		self.execute(context)
		return {'FINISHED'}
	
	def execute(op, context):
		esconde.esconde('luz.', False)

		return {'FINISHED'}

def register():
	bpy.utils.register_module(__name__)

	pass
	
def unregister():
	bpy.utils.unregister_module(__name__)

	pass
	
if __name__ == "__main__":
	register()
