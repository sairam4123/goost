#pragma once

#include "scene/main/node.h"

class Spawner : public Node {
	GDCLASS(Spawner, Node);

public:
	enum ProcessMode {
		PROCESS_PHYSICS,
		PROCESS_IDLE,
	};

private:
	Ref<Resource> resource;

	bool spawning = true;

	uint32_t rate = 1; // Objects per time `step`.
	double step = 1.0; // The `rate` amount of objects will be spawned each time step.
	double delay = 0.0; // Before spawning starts.
	// double lifetime = 0.0; // Lifetime of each object before destroying an object.
	uint32_t limit = 0; // Before spawning stops, zero means unlimited.

	ProcessMode process_mode = PROCESS_IDLE;

	// Internal.
	double time = 0.0;
	double delay_time = 0.0;
	uint32_t amount = 0;

protected:
	void _notification(int p_what);
	static void _bind_methods();

	void _process_spawn();
	void _set_process(bool p_process);

public:
	void set_resource(const Ref<Resource> &p_resource);
	Ref<Resource> get_resource() const { return resource; }

	void set_spawning(bool p_spawning);
	bool is_spawning() const { return spawning; }

	Node *spawn();

	void set_rate(int p_rate);
	int get_rate() const { return rate; }

	void set_step(double p_step);
	double get_step() const { return step; }

	void set_delay(double p_delay);
	double get_delay() const { return delay; }

	// void set_lifetime(double p_lifetime);
	// double get_lifetime() const { return lifetime; }

	void set_limit(int p_limit);
	int get_limit() const { return limit; }

	void set_process_mode(ProcessMode p_mode);
	ProcessMode get_process_mode() const { return process_mode; };
};

VARIANT_ENUM_CAST(Spawner::ProcessMode);
