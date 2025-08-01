<script lang="ts">
	import { cedulaMask, DataTable, maxYearDate, nota, ConfirmDeleteModal, StatusToggleModal } from '$lib';
	import { imask } from '@imask/svelte';
	import {
		Button,
		Checkbox,
		Input,
		Label,
		Modal,
		Select,
		TableSearch,
		Textarea,
		Datepicker,

		Tooltip

	} from 'flowbite-svelte';
	import { EyeOutline, FileCopyOutline, PenOutline, PlusOutline, UsersOutline, CheckOutline } from 'flowbite-svelte-icons';
	import type { Estudiante } from '../../../app';
	import { resolver } from '$lib/utilidades/resolver';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { enhance } from '$app/forms';
	import ToastContainer from '$lib/componentes/ToastContainer.svelte';
	import { pl } from 'date-fns/locale';

	// Datos de la página
	let { data } = $props();

	// Estado para el modal
	let modalVisible = $state(false);
	let isEditing = $state(false);
	let searchTerm = $state('');
	let formEl: HTMLFormElement | undefined = $state();
	// Estado para el modal de confirmación de eliminación
	let deleteModalOpen = $state(false);
	let selectedStudentForDelete: Estudiante | null = $state(null);
	
	// Estado para el modal de activación/desactivación
	let statusModalOpen = $state(false);
	let selectedStudentForStatus: Estudiante | null = $state(null);
	let statusModalTitle = $state('');
	let statusModalMessage = $state('');
	let estudianteActual: Partial<{
		id: number;
		cedula: string;
		nombre: string;
		correo: string;
		activo: boolean;
		semestre: number;
		carrera: number;
		promedio: number;
		direccion: string;
		fecha_nac: Date;
		sexo: 'M' | 'F' | '';
		usuario?: {
			id: number;
		};
	}> = $state({});

	$effect(() => {
		if (!modalVisible) {
			estudianteActual = {};
		}
	});

	$effect(() => {
		if (data.estudiantes) {
			estudiantesFiltrados =
				data?.estudiantes.filter(
					(est) =>
						est?.nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est?.cedula?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est?.correo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
						est.direccion.toLowerCase().includes(searchTerm.toLowerCase())
				) ?? [];
		}
	});

	let estudiantes: Estudiante[] = $state(data.estudiantes);
	let estudiantesFiltrados = $derived(
		estudiantes.filter(
			(est) =>
				est?.nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est?.cedula?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est?.correo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
				est.direccion.toLowerCase().includes(searchTerm.toLowerCase())
		) ?? []
	);

	// Función para abrir el modal en modo edición
	function editarEstudiante(estudiante: any) {
		estudianteActual = {
			...estudiante,
			carrera: data.carreras.find((car) => car.nombre === estudiante.carrera)?.id || 1,
			fecha_nac: new Date(estudiante.fecha_nacimiento),
			fecha_nacimiento: undefined
		};
		isEditing = true;
		modalVisible = true;
	}

	// Función para abrir el modal en modo creación
	function crearEstudiante() {
		estudianteActual = {
			id: 0,
			cedula: '',
			nombre: '',
			correo: '',
			activo: true,
			semestre: 1,
			carrera: 1,
			promedio: 0,
			direccion: '',
			fecha_nac: maxYearDate(),
			sexo: 'M'
		};
		isEditing = false;
		modalVisible = true;
	}

	function calcularEdad(fechaNacimiento: Date | null = null): number {
		if (!fechaNacimiento) return 0;

		const hoy = new Date();
		const nacimiento = fechaNacimiento;

		let edad = hoy.getFullYear() - nacimiento.getFullYear();
		const mes = hoy.getMonth() - nacimiento.getMonth();

		if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
			edad--;
		}

		return edad;
	}

	// Actualizar edad cuando cambia la fecha de nacimiento
	let edad = $derived(calcularEdad(estudianteActual?.fecha_nac || null));

	// Función para abrir el modal de confirmación de eliminación
	function confirmarEliminarEstudiante(estudiante: Estudiante) {
		selectedStudentForDelete = estudiante;
		deleteModalOpen = true;
	}
	
	// Función para abrir el modal de activación/desactivación
	function confirmarCambiarEstadoEstudiante(estudiante: Estudiante) {
		selectedStudentForStatus = estudiante;
		statusModalTitle = estudiante.activo ? "Inactivar Estudiante" : "Activar Estudiante";
		statusModalMessage = estudiante.activo ? 
			`¿Estás seguro de que deseas inactivar al estudiante ${estudiante.nombre}?` : 
			`¿Estás seguro de que deseas activar al estudiante ${estudiante.nombre}?`;
		statusModalOpen = true;
	}
	
	const handleSuccess = () => {
		// Refresh data after successful toggle
		estudiantes = data.estudiantes;
	};

	const handleSubmit: SubmitFunction = () => {
		return resolver(() => {
			if (isEditing) {
				modalVisible = false;
			}
		});
	};
</script>

<div class="w-full">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Estudiantes</h1>
		{#if data.rol !== 'coordinador' && data.rol !== 'caja'}
			<Button color="blue" onclick={crearEstudiante}>
				<PlusOutline class="mr-2 h-5 w-5" />
				Registrar
			</Button>
		{/if}
	</div>

	<div class="mb-4">
		<TableSearch bind:inputValue={searchTerm} placeholder="Buscar por nombre, cédula o correo..." />
	</div>

	{#snippet actions(row: Estudiante)}
		<div class="flex gap-2">
			{#if data.rol !== 'coordinador' && data.rol !== 'caja'}
				<div class="relative">
					<Button pill size="xs" class="p-1.5!" color="light" onclick={() => editarEstudiante(row)}>
						<PenOutline class="w-5 h-5" />
					</Button>
					<Tooltip placement="top">Editar estudiante</Tooltip>
				</div>
				<div class="relative">
					<Button
						pill
						class="p-1.5!"
						size="xs"
						color={row.activo ? "red" : "green"}
						onclick={() => confirmarCambiarEstadoEstudiante(row)}
					>
						{#if row.activo}
							<UsersOutline class="w-5 h-5" />
						{:else}
							<CheckOutline class="w-5 h-5" />
						{/if}
					</Button>
					<Tooltip placement="top">{row.activo ? "Inactivar estudiante" : "Activar estudiante"}</Tooltip>
				</div>
			{/if}
			<div class="relative">
				<Button pill size="xs" class="p-1.5!" color="blue" onclick={() => navigator.clipboard.writeText(row.cedula || '')}>
					<FileCopyOutline class="w-5 h-5" />
				</Button>
				<Tooltip placement="top">Copiar cédula</Tooltip>
			</div>
		</div>
	{/snippet}
	<DataTable data={estudiantesFiltrados} {actions}></DataTable>

	<Modal
		title={isEditing ? 'Editar Estudiante' : 'Nuevo Estudiante'}
		bind:open={modalVisible}
		size="xl"
	>
		<form
			action={isEditing ? '?/edit' : '?/create'}
			method="POST"
			use:enhance={handleSubmit}
			bind:this={formEl}
		>
			{#if isEditing}
				<input type="hidden" name="id_estudiante" value={estudianteActual!.id} />
				<input type="hidden" name="id" value={estudianteActual!.usuario?.id} />
			{/if}

			<div class="grid grid-cols-1 md:grid-cols-6 gap-4 mb-4">
				<div class="md:col-span-2">
					<Label for="cedula" class="mb-2">Cédula</Label>
					<input
						id="cedula"
						name="cedula"
						placeholder="Ingrese la cédula"
						value={estudianteActual?.cedula || ''}
						oninput={(e) => {
							if (estudianteActual) estudianteActual.cedula = e.currentTarget.value;
						}}
						required
						use:imask={cedulaMask as any}
						class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="nombre" class="mb-2">Nombre Completo</Label>
					<Input
						id="nombre"
						name="nombre"
						placeholder="Ingrese el nombre completo"
						value={estudianteActual?.nombre || ''}
						required
						oninput={(e: Event) => {
							const target = e.currentTarget as HTMLInputElement;
							if (estudianteActual && target) estudianteActual.nombre = target.value.replace(/\d+/g, '');
						}}
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="fecha_nac" class="mb-2">Fecha de Nacimiento</Label>
					<Datepicker
						availableTo={maxYearDate()}
						placeholder="Seleccione una fecha"
						bind:value={estudianteActual.fecha_nac}
						translationLocale="es-VE"
						locale="fr-FR"
						inputmode="numeric"
						dateFormat={{ year: 'numeric', month: '2-digit', day: '2-digit' }}
					/>
					<input
						type="hidden"
						name="fecha_nac"
						value={estudianteActual.fecha_nac ? estudianteActual.fecha_nac.toISOString().split('T')[0] : ''}
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="correo" class="mb-2">Correo Electrónico</Label>
					<Input
						id="correo"
						name="correo"
						type="email"
						placeholder="correo@ejemplo.com"
						value={estudianteActual?.correo}
						required
					/>
				</div>
				<div class="md:col-span-2">
					<Label for="carrera" class="mb-2">Carrera</Label>
					<Select
						id="carrera"
						name="carrera"
						placeholder="Seleccionar"
						value={estudianteActual?.carrera}
						required
						items={data.carreras.map((carrera) => ({
							value: carrera.id,
							name: carrera.nombre
						}))}
					/>
				</div>
				<div>
					<Label for="sexo" class="mb-2">Sexo</Label>
					<Select
						id="sexo"
						name="sexo"
						placeholder="Seleccionar"
						value={estudianteActual?.sexo}
						required
						items={[
							{ value: 'M', name: 'Masculino' },
							{ value: 'F', name: 'Femenino' }
						]}
					/>
				</div>
				<div>
					<Label for="semestre" class="mb-2">Semestre</Label>
					<Select
						id="semestre"
						name="semestre"
						placeholder="Seleccionar"
						value={estudianteActual?.semestre}
						required
						items={Array(10)
							.fill(null)
							.map((_, i) => ({ value: i + 1, name: `${i + 1}° Semestre` }))}
					/>
				</div>
				<div>
					<Label for="promedio" class="mb-2">Promedio</Label>
					<input
						id="promedio"
						name="promedio"
						type="number"
						class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500"
						use:imask={nota}
						value={estudianteActual?.promedio || 0}
						required
					/>
				</div>
				<div>
					<Label for="edad" class="mb-2">Edad</Label>
					<Input id="edad" name="edad" type="number" value={edad} readonly />
				</div>
				<div class={!isEditing ? 'md:col-span-5' : 'md:col-span-4 row-span-2'}>
					<Label for="direccion" class="mb-2">Dirección</Label>
					<Textarea
						id="direccion"
						name="direccion"
						placeholder="Ingrese la dirección completa"
						value={estudianteActual?.direccion}
						rows={3}
					/>
				</div>
				{#if isEditing}
					<div class="flex items-center">
						<Checkbox id="activo" name="activo" checked={estudianteActual?.activo} />
						<Label for="activo" class="ml-2">Usuario Activo</Label>
					</div>
				{/if}
			</div>
		</form>
		{#snippet footer()}
			<div class="flex justify-between items-center w-full">
				<div>
					<Button type="button" color="alternative" onclick={() => (modalVisible = false)}
						>Cancelar</Button
					>
					<Button type="submit" color="primary" onclick={() => formEl && formEl.requestSubmit()}
						>{isEditing ? 'Actualizar' : 'Guardar'}</Button
					>
				</div>
				<ToastContainer />
			</div>
		{/snippet}
	</Modal>

	<!-- Modal de confirmación de eliminación -->
	<ConfirmDeleteModal
		bind:open={deleteModalOpen}
		title="Eliminar Estudiante"
		message="¿Estás seguro de que deseas eliminar al estudiante {selectedStudentForDelete?.nombre}? Esta acción no se puede deshacer."
		action="?/delete"
		formData={{ cedula: selectedStudentForDelete?.cedula || '' }}
		onSuccess={() => {
			selectedStudentForDelete = null;
		}}
	/>
	
	<!-- Modal de confirmación de activación/desactivación -->
	<StatusToggleModal
		bind:open={statusModalOpen}
		title={statusModalTitle}
		message={statusModalMessage}
		action="?/toggleStatus"
		formData={{
			cedula: selectedStudentForStatus?.cedula || ''
		}}
		isActivating={selectedStudentForStatus ? !selectedStudentForStatus.activo : false}
		onSuccess={handleSuccess}
	/>
</div>
