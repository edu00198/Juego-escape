# TODO for Modifying Map 1 Code Input at Door

- [x] Modify door collision in mapa_1.py: Change condition to show code panel when chest is open
- [x] Update event handling: When code correct, call ejecutar_mapa2() instead of setting puerta_abierta
- [x] Remove unused variables: puerta_abierta and puerta_dialog_shown
- [x] Improve graphical design of code input panel
- [x] Position code panel over player when spawning
- [x] Prevent code panel from appearing when returning from mapa2
- [x] Ensure interface is invisible and player can move freely when returning to mapa1 after correct code
- [ ] Test the changes to ensure code input appears at door after chest open, and correct code leads to map2
