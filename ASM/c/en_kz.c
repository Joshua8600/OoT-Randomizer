#include "z64.h"
#include "actor.h"


typedef enum BOULDER_TYPE {
    BOULDER_TYPE_BROWN = 0,
    BOULDER_TYPE_BRONZE = 1,
    BOULDER_TYPE_SILVER = 2,
    BOULDER_TYPE_RED_ICE = 3,
    BOULDER_TYPE_HEAVY_BLOCK = 4,
};

uint8_t KZ_BOULDER_TYPE;
extern uint16_t CURR_ACTOR_SPAWN_INDEX;
extern uint8_t CFG_BOULDER_SHUFFLE;
extern int8_t curr_scene_setup;
extern xflag_t* spawn_actor_with_flag;
extern void EnKz_Update(z64_actor_t* this, z64_game_t* globalCtx);
typedef void(*ActorUpdateFunc)(z64_actor_t* this, z64_game_t* globalCtx);

z64_actor_t* EnKz_SpawnRedIce_Hook(z64_actor_ctxt_t* actorCtx, z64_actor_t* parent, z64_game_t* globalCtx, int16_t actorId, float posX, float posY, float posZ, int16_t rotX, int16_t rotY, int16_t rotZ, int16_t params) {

    z64_actor_t* spawned = NULL;
    if(CFG_BOULDER_SHUFFLE) {
        xflag_t flag;
        flag.scene = globalCtx->scene_index;
        flag.room = parent->room_index;
        flag.setup = curr_scene_setup;
        flag.flag = 1;
        flag.subflag = 1;
        spawn_actor_with_flag = &flag;
        switch(KZ_BOULDER_TYPE) {
            case BOULDER_TYPE_BROWN:
                spawned = Actor_SpawnAsChild(actorCtx, parent, globalCtx, ACTOR_OBJ_BOMBIWA, posX, posY, posZ, rotX, rotY, rotZ, 0x3F);
                break;
            case BOULDER_TYPE_BRONZE:
                spawned = Actor_SpawnAsChild(actorCtx, parent, globalCtx, ACTOR_OBJ_HAMISHI, posX, posY, posZ, rotX, rotY, rotZ, 0x3F);
                break;
            case BOULDER_TYPE_SILVER:
                spawned = Actor_SpawnAsChild(actorCtx, parent, globalCtx, ACTOR_EN_ISHI, posX, posY, posZ, rotX, rotY, rotZ, 0xF0C1);
                spawned->parent = NULL;
                break;
            case BOULDER_TYPE_RED_ICE:
                spawned = Actor_SpawnAsChild(actorCtx, parent, globalCtx, actorId, posX, posY, posZ, rotX, rotY, rotZ, params);
                break;
            case BOULDER_TYPE_HEAVY_BLOCK:
                spawned = NULL;
                break;
            default:
                spawned = Actor_SpawnAsChild(actorCtx, parent, globalCtx, actorId, posX, posY, posZ, rotX, rotY, rotZ, params);
                break;
        }
        spawn_actor_with_flag = NULL;
        return spawned;
    }
    return Actor_SpawnAsChild(actorCtx, parent, globalCtx, actorId, posX, posY, posZ, rotX, rotY, rotZ, params);
}

void EnKz_Update_Hook(z64_actor_t* this, z64_game_t* globalCtx) {
    ActorUpdateFunc EnKz_Update = Actor_ResolveOverlayAddr(this, 0x80ad6d70);
    if(CFG_BOULDER_SHUFFLE) {
        if((this->child == NULL) || (this->child->update == NULL)) {
            this->child = NULL;
            EnKz_Update(this, globalCtx);
        }
    }
    else {
        EnKz_Update(this, globalCtx);
    }
}
