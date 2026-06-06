/**
 * Servicio de Tracking de Personas
 * Mantiene un registro de personas detectadas y su historial de movimientos
 */

class PersonTracker {
  constructor(maxTrackedPersons = 5, trackingTimeout = 5000) {
    this.trackedPersons = new Map(); // id -> person data
    this.personCounter = 0;
    this.maxTrackedPersons = maxTrackedPersons;
    this.trackingTimeout = trackingTimeout;
    this.frameHistory = [];
    this.maxHistory = 30; // 30 frames de historial
  }

  /**
   * Calcula distancia euclidiana entre dos puntos
   */
  distance(point1, point2) {
    const dx = point1.x - point2.x;
    const dy = point1.y - point2.y;
    return Math.sqrt(dx * dx + dy * dy);
  }

  /**
   * Calcula IOU (Intersection over Union) entre dos cajas
   */
  calculateIOU(box1, box2) {
    const x1_min = box1.x;
    const y1_min = box1.y;
    const x1_max = box1.x + box1.w;
    const y1_max = box1.y + box1.h;

    const x2_min = box2.x;
    const y2_min = box2.y;
    const x2_max = box2.x + box2.w;
    const y2_max = box2.y + box2.h;

    const intersect_w = Math.max(0, Math.min(x1_max, x2_max) - Math.max(x1_min, x2_min));
    const intersect_h = Math.max(0, Math.min(y1_max, y2_max) - Math.max(y1_min, y2_min));
    const intersect_area = intersect_w * intersect_h;

    const box1_area = box1.w * box1.h;
    const box2_area = box2.w * box2.h;
    const union_area = box1_area + box2_area - intersect_area;

    return union_area > 0 ? intersect_area / union_area : 0;
  }

  /**
   * Encuentra el mejor emparejamiento entre detecciones y personas rastreadas
   */
  matchDetections(detections) {
    const matches = [];
    const matched = new Set();

    for (const tracked of this.trackedPersons.values()) {
      if (Date.now() - tracked.lastSeen > this.trackingTimeout) continue;

      let bestMatch = null;
      let bestScore = 0.3; // Umbral mínimo IOU

      detections.forEach((detection, idx) => {
        if (matched.has(idx)) return;

        const iou = this.calculateIOU(tracked.box, detection.face_box);
        if (iou > bestScore) {
          bestScore = iou;
          bestMatch = idx;
        }
      });

      if (bestMatch !== null) {
        matches.push({ trackedId: tracked.id, detectionIdx: bestMatch, score: bestScore });
        matched.add(bestMatch);
      }
    }

    return { matches, unmatchedDetections: detections.map((_, i) => i).filter(i => !matched.has(i)) };
  }

  /**
   * Actualiza el tracking con nuevas detecciones
   */
  updateTracking(detections) {
    const { matches, unmatchedDetections } = this.matchDetections(detections);
    const timestamp = Date.now();

    // Actualizar personas rastreadas existentes
    matches.forEach(({ trackedId, detectionIdx }) => {
      const person = this.trackedPersons.get(trackedId);
      const detection = detections[detectionIdx];

      person.lastSeen = timestamp;
      person.box = detection.face_box;
      person.detectionHistory.push({
        timestamp,
        attention_score: detection.attention_score,
        orientation: detection.head_orientation,
        distracted: detection.distracted,
      });

      // Mantener historial limitado
      if (person.detectionHistory.length > this.maxHistory) {
        person.detectionHistory.shift();
      }

      person.framesSinceLastSeen = 0;
      person.averageAttentionScore =
        person.detectionHistory.reduce((sum, h) => sum + h.attention_score, 0) /
        person.detectionHistory.length;
    });

    // Crear nuevas personas para detecciones no emparejadas
    unmatchedDetections.forEach((idx) => {
      if (this.trackedPersons.size < this.maxTrackedPersons) {
        const personId = ++this.personCounter;
        const detection = detections[idx];

        this.trackedPersons.set(personId, {
          id: personId,
          box: detection.face_box,
          detectionHistory: [
            {
              timestamp,
              attention_score: detection.attention_score,
              orientation: detection.head_orientation,
              distracted: detection.distracted,
            },
          ],
          lastSeen: timestamp,
          framesSinceLastSeen: 0,
          averageAttentionScore: detection.attention_score,
          createdAt: timestamp,
        });
      }
    });

    // Incrementar contador para personas no detectadas
    this.trackedPersons.forEach((person) => {
      if (person.lastSeen < timestamp - 100) {
        person.framesSinceLastSeen++;
      }
    });

    // Eliminar personas que no se han visto en mucho tiempo
    for (const [id, person] of this.trackedPersons.entries()) {
      if (timestamp - person.lastSeen > this.trackingTimeout) {
        this.trackedPersons.delete(id);
      }
    }

    return {
      trackedPersons: Array.from(this.trackedPersons.values()),
      totalTracked: this.trackedPersons.size,
      timestamp,
    };
  }

  /**
   * Obtiene estadísticas de una persona rastreada
   */
  getPersonStats(personId) {
    const person = this.trackedPersons.get(personId);
    if (!person) return null;

    const history = person.detectionHistory;
    if (history.length === 0) return null;

    const attentionScores = history.map((h) => h.attention_score);
    const distractedCount = history.filter((h) => h.distracted).length;

    return {
      personId: person.id,
      framesTracked: history.length,
      averageAttentionScore: person.averageAttentionScore,
      maxAttentionScore: Math.max(...attentionScores),
      minAttentionScore: Math.min(...attentionScores),
      distractedFrames: distractedCount,
      distractedPercentage: (distractedCount / history.length) * 100,
      trackedDuration: person.lastSeen - person.createdAt,
    };
  }

  /**
   * Obtiene todas las estadísticas
   */
  getAllStats() {
    const stats = [];
    for (const [id] of this.trackedPersons.entries()) {
      const personStats = this.getPersonStats(id);
      if (personStats) stats.push(personStats);
    }
    return stats;
  }

  /**
   * Limpia el tracking
   */
  reset() {
    this.trackedPersons.clear();
    this.frameHistory = [];
    this.personCounter = 0;
  }
}

export default PersonTracker;
