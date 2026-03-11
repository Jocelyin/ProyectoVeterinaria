import { useState } from 'preact/hooks';

const API_URL = 'http://localhost:8000';

export default function ReportForm() {
    const [tipo, setTipo] = useState('citas');
    const [fechaInicio, setFechaInicio] = useState('');
    const [fechaFin, setFechaFin] = useState('');
    const [estado, setEstado] = useState('idle'); // idle | generating | done | error
    const [progreso, setProgreso] = useState(0);
    const [error, setError] = useState('');
    const [totalRegistros, setTotalRegistros] = useState(null);

    // Max date = today
    const today = new Date().toISOString().split('T')[0];

    const resetState = () => {
        setEstado('idle');
        setProgreso(0);
        setError('');
        setTotalRegistros(null);
    };

    const downloadReport = async (formato) => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            setError('Sesión expirada. Inicia sesión de nuevo.');
            setEstado('error');
            return;
        }

        if (!fechaInicio || !fechaFin) {
            setError('Selecciona ambas fechas.');
            setEstado('error');
            return;
        }

        if (fechaInicio > fechaFin) {
            setError('La fecha de inicio no puede ser mayor a la fecha fin.');
            setEstado('error');
            return;
        }

        setEstado('generating');
        setError('');
        setProgreso(0);

        // Simulate progress animation
        let prog = 0;
        const progressInterval = setInterval(() => {
            prog += Math.random() * 15 + 5;
            if (prog > 90) prog = 90;
            setProgreso(Math.round(prog));
        }, 300);

        try {
            const res = await fetch(`${API_URL}/api/reports`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    tipo,
                    fecha_inicio: fechaInicio,
                    fecha_fin: fechaFin,
                    formato
                })
            });

            clearInterval(progressInterval);

            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.detail || 'Error al generar el reporte');
            }

            setProgreso(100);

            // Download the file
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            const ext = formato === 'pdf' ? 'pdf' : 'xlsx';
            a.download = `reporte_${tipo}_${fechaInicio}_${fechaFin}.${ext}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            setTimeout(() => {
                setEstado('done');
            }, 400);

        } catch (e) {
            clearInterval(progressInterval);
            setError(e.message || 'Error desconocido');
            setEstado('error');
        }
    };

    const tipoLabels = {
        citas: '📅 Citas',
        clientes: '👥 Clientes',
        pacientes: '🐾 Pacientes'
    };

    return (
        <div>
            <h3 class="settings-panel-title">Reportes</h3>
            <p class="settings-panel-desc">
                Genera reportes de tu veterinaria en formato PDF o Excel. Los datos se obtienen directamente del sistema.
            </p>

            {/* Form */}
            <div class="report-form-container">
                {/* Tipo de reporte */}
                <div class="settings-field">
                    <label class="settings-label">Tipo de reporte</label>
                    <select
                        class="settings-input"
                        value={tipo}
                        onChange={(e) => { setTipo(e.target.value); resetState(); }}
                    >
                        <option value="citas">📅 Citas</option>
                        <option value="clientes">👥 Clientes</option>
                        <option value="pacientes">🐾 Pacientes (Mascotas)</option>
                    </select>
                </div>

                {/* Fechas */}
                <div class="report-dates-row">
                    <div class="settings-field" style={{ flex: 1 }}>
                        <label class="settings-label">Fecha inicio</label>
                        <input
                            type="date"
                            class="settings-input"
                            value={fechaInicio}
                            max={today}
                            onKeyDown={(e) => e.preventDefault()}
                            onChange={(e) => { setFechaInicio(e.target.value); resetState(); }}
                        />
                    </div>
                    <div class="settings-field" style={{ flex: 1 }}>
                        <label class="settings-label">Fecha fin</label>
                        <input
                            type="date"
                            class="settings-input"
                            value={fechaFin}
                            max={today}
                            min={fechaInicio || undefined}
                            onKeyDown={(e) => e.preventDefault()}
                            onChange={(e) => { setFechaFin(e.target.value); resetState(); }}
                        />
                    </div>
                </div>

                {/* Info text */}
                <p class="report-info-text">
                    📋 Se generará un reporte de <strong>{tipoLabels[tipo]}</strong> con los datos registrados en el sistema
                    {fechaInicio && fechaFin ? ` del ${fechaInicio} al ${fechaFin}` : ''}.
                </p>

                {/* Download buttons */}
                <div class="report-action-row">
                    <button
                        class="report-download-btn report-btn-pdf"
                        onClick={() => downloadReport('pdf')}
                        disabled={estado === 'generating' || !fechaInicio || !fechaFin}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                            <polyline points="14 2 14 8 20 8" />
                            <line x1="16" y1="13" x2="8" y2="13" />
                            <line x1="16" y1="17" x2="8" y2="17" />
                            <polyline points="10 9 9 9 8 9" />
                        </svg>
                        Generar PDF
                    </button>
                    <button
                        class="report-download-btn report-btn-excel"
                        onClick={() => downloadReport('excel')}
                        disabled={estado === 'generating' || !fechaInicio || !fechaFin}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                            <line x1="9" y1="3" x2="9" y2="21" />
                            <line x1="15" y1="3" x2="15" y2="21" />
                            <line x1="3" y1="9" x2="21" y2="9" />
                            <line x1="3" y1="15" x2="21" y2="15" />
                        </svg>
                        Generar Excel
                    </button>
                </div>
            </div>

            {/* Progress Bar */}
            {estado === 'generating' && (
                <div class="report-status-section">
                    <p class="report-status-text">⏳ Generando reporte...</p>
                    <div class="report-progress-bar">
                        <div
                            class="report-progress-fill"
                            style={{ width: `${progreso}%` }}
                        />
                    </div>
                    <p class="report-progress-percent">{progreso}%</p>
                </div>
            )}

            {/* Done */}
            {estado === 'done' && (
                <div class="report-status-section report-status-done">
                    <div class="report-done-icon">✅</div>
                    <p class="report-status-text" style={{ color: '#10b981' }}>
                        ¡Reporte generado y descargado exitosamente!
                    </p>
                    <p class="report-info-text" style={{ marginTop: '0.5rem' }}>
                        Puedes generar otro reporte cambiando los filtros o el formato.
                    </p>
                </div>
            )}

            {/* Error */}
            {estado === 'error' && (
                <div class="report-status-section report-status-error">
                    <p class="report-status-text" style={{ color: '#ef4444' }}>
                        ❌ {error}
                    </p>
                    <button
                        class="settings-btn-secondary"
                        style={{ marginTop: '0.75rem', fontSize: '0.8rem' }}
                        onClick={resetState}
                    >
                        Intentar de nuevo
                    </button>
                </div>
            )}
        </div>
    );
}
