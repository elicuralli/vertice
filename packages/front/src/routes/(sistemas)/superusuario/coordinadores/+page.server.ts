import {
	actualizarCoordinador,
	actualizarUsuario,
	crearCoordinador,
	crearUsuario,
	eliminarCoordinador,
	obtenerCarreras,
	obtenerCoordinadores,
	type CoordinadorReq
} from '$lib';
import type { Usuario } from '../../../../app';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	try {
		const carreras = await obtenerCarreras(fetch);
		const res = await obtenerCoordinadores(fetch);
		console.log('coordinadores', res);
		return { coordinadores: res, carreras };
	} catch (error) {
		console.error('Error al obtener carreras:', error);
		return { carreras: [], coordinadores: [] };
	}
};

export const actions: Actions = {
	// Acción para crear un usuario y un coordinador
	create: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as CoordinadorReq &
			Usuario;
		
		const usuario: Partial<Usuario & { password: string; rol_id: number }> = {
			id: 0,
			cedula: payload.cedula,
			correo: payload.correo,
			activo: true,
			nombre: payload.nombre,
			password: payload.password,
			rol_id: 4
		};

		try {
			const { data }: { data: Usuario } = await crearUsuario(fetch, usuario);
			usuario.id = data.id;
		} catch (error) {
			console.error('Error al crear carrera:', error);
			return { errores: { form: 'Error al crear el usuario' } };
		}

		const coordinador: CoordinadorReq = {
			carrera_id: payload.carrera_id,
			usuario_id: usuario.id,
			telefono: payload.telefono
		};

		try {
			await crearCoordinador(fetch, coordinador);
			return { coordinador: usuario.nombre };
		} catch (e) {
			console.error(e);
			return { errores: { form: 'Error al crear el coordinador' } };
		}
	},

	edit: async ({ request, fetch }) => {
		const payload = Object.fromEntries(await request.formData()) as unknown as CoordinadorReq &
			Usuario & { id_coordinador: number };
		
		const usuario: Partial<Usuario & { password: string; rol_id: number }> = {
			cedula: payload.cedula,
			correo: payload.correo,
			activo: true,
			nombre: payload.nombre,
			rol_id: 4
		};

		try {
			await actualizarUsuario(fetch, payload.id, usuario);
		} catch (error) {
			console.error('Error al editar usuario:', error);
			return { errores: { form: 'Error al editar el usuario' } };
		}

		const coordinador: CoordinadorReq = {
			carrera_id: payload.carrera_id,
			telefono: payload.telefono
		};

		try {
			await actualizarCoordinador(fetch, payload.id_coordinador, coordinador);
			return { coordinador: usuario.nombre };
		} catch (e) {
			console.error(e);
			return { errores: { form: 'Error al editar el coordinador' } };
		}
	},

	delete: async ({ request, fetch }) => {
		const formData = await request.formData();
		const cedula = formData.get('cedula')?.toString() || '';

		try {
			const res = await eliminarCoordinador(fetch, cedula);
			console.log('carrera eliminada', res);
			return { exito: true };
		} catch (error) {
			console.error('Error al eliminar carrera:', error);
			return { errores: { form: 'Error al eliminar la carrera' } };
		}
	}
};
