# Lancer le serveur en processus détaché et permanent
$path = 'C:\Users\eisbr\Nouveau dossier'
cd $path

# Tuer les anciens serveurs
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Lancer le serveur en processus détaché (reste actif même si PowerShell ferme)
Write-Host "Lancement du serveur sur le port 3000..."
Start-Process -FilePath "python" -ArgumentList "start_with_waitress.py" -WorkingDirectory $path -WindowStyle Hidden -PassThru

Start-Sleep -Seconds 3

# Vérifier que le serveur répond
Write-Host "Vérification du serveur..."
$attempt = 0
while ($attempt -lt 5) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000/" -UseBasicParsing -ErrorAction Stop -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✓ Serveur OK sur http://localhost:3000/" -ForegroundColor Green
            Write-Host "✓ Accédez via ngrok: https://crispate-clementina-uretic.ngrok-free.dev/" -ForegroundColor Green
            exit 0
        }
    } catch {
        $attempt++
        if ($attempt -lt 5) {
            Write-Host "  Tentative $attempt/5..."
            Start-Sleep -Seconds 2
        }
    }
}

Write-Host "✗ Serveur ne répond pas après 10 secondes" -ForegroundColor Red
exit 1
