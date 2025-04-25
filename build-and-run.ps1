# PowerShell script to build and run the monitoring stack

Write-Host "Building and starting the monitoring stack..." -ForegroundColor Green

# Build the Docker images
Write-Host "Building Docker images..." -ForegroundColor Cyan
docker-compose build

# Start the containers
Write-Host "Starting containers..." -ForegroundColor Cyan
docker-compose up -d

# Wait for services to be ready
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if services are running
Write-Host "Checking service status..." -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "Monitoring stack is now running!" -ForegroundColor Green
Write-Host ""
Write-Host "Access the services at:" -ForegroundColor White
Write-Host "- Webapp: http://localhost:8080" -ForegroundColor White
Write-Host "- Prometheus: http://localhost:9090" -ForegroundColor White
Write-Host "- Alertmanager: http://localhost:9093" -ForegroundColor White
Write-Host "- Grafana: http://localhost:3001 (username: admin, password: admin)" -ForegroundColor White
Write-Host ""
Write-Host "To view logs, run: docker-compose logs -f" -ForegroundColor Yellow
Write-Host "To stop the stack, run: docker-compose down" -ForegroundColor Yellow
Write-Host ""
Write-Host "Note: Make sure the Windows Exporter is running on port 9182" -ForegroundColor Magenta
Write-Host "      You can verify this by visiting http://localhost:9182/metrics" -ForegroundColor Magenta 