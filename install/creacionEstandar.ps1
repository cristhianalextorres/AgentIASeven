# Ruta base del proyecto
$basePath = $PSScriptRoot

# Crear carpetas estándar
$folders = @("data", "install", "logs", "src", "test")
foreach ($folder in $folders) {
    $fullPath = Join-Path -Path $basePath -ChildPath $folder
    if (-Not (Test-Path -Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath | Out-Null
        Write-Host "Carpeta creada: $fullPath"
    } else {
        Write-Host "Ya existe: $fullPath"
    }
}

# Crear archivos estándar
$readmePath = Join-Path -Path $basePath -ChildPath "README.md"
$requirementsPath = Join-Path -Path $basePath -ChildPath "requirements.txt"

if (-Not (Test-Path $readmePath)) {
    Set-Content -Path $readmePath -Value "# Proyecto: Tablero ISC`n`nDescripción del proyecto."
    Write-Host "Archivo creado: README.md"
} else {
    Write-Host "Ya existe: README.md"
}

if (-Not (Test-Path $requirementsPath)) {
    Set-Content -Path $requirementsPath -Value "# Requerimientos del proyecto"
    Write-Host "Archivo creado: requirements.txt"
} else {
    Write-Host "Ya existe: requirements.txt"
}
