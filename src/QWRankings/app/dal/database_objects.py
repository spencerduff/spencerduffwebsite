from datetime import datetime
import dataclasses


@dataclasses.dataclass
class MatchInfo:
    match_id: str
    date: datetime
    mode: str
    map: str


@dataclasses.dataclass
class RatingAndRank:
    rating: float
    ratings_deviation: float
    rank: int


@dataclasses.dataclass
class PlayerMatchRanking:
    match_info: MatchInfo
    match_user_id: str
    name: str
    login: str
    overall_rating_and_rank: RatingAndRank
    map_rating_and_rank: RatingAndRank
    win: int


@dataclasses.dataclass
class PlayerRanking:
    overall_rating_and_rank: RatingAndRank
    map_rating_and_rank: RatingAndRank


@dataclasses.dataclass
class WeaponStats:
    weapon_name: str
    acc_attacks: float
    acc_hits: float
    acc_real: float
    acc_virtual: float
    kills_total: float
    kills_team: float
    kills_enemy: float
    kills_self: float
    deaths: float
    pickups_dropped: float
    pickups_taken: float
    pickups_total_taken: float
    pickups_spawn_taken: float
    pickups_spawn_total_taken: float
    dmg_enemy: float
    dmg_team: float


@dataclasses.dataclass
class ItemStats:
    hp_15_took: float
    hp_25_took: float
    hp_100_took: float
    ga_took: float
    ga_time: float
    ya_took: float
    ya_time: float
    ra_took: float
    ra_time: float
    q_took: float
    q_time: float
    p_took: float
    p_time: float
    r_took: float
    r_time: float


@dataclasses.dataclass
class PlayerStats:
    ping: float
    frags: float
    deaths: float
    tk: float
    spawn_frags: float
    kills: float
    suicides: float
    dmg_taken: float
    dmg_given: float
    dmg_team: float
    dmg_self: float
    dmg_team_weap: float
    dmg_enemy_weap: float
    dmg_taken_to_die: float
    xfer_rl: float
    xfer_lg: float
    spree_max: float
    spree_quad: float
    control: float
    speed_max: float
    speed_avg: float
    item_stats: ItemStats
    axe_stats: WeaponStats
    sg_stats: WeaponStats
    ssg_stats: WeaponStats
    ng_stats: WeaponStats
    sng_stats: WeaponStats
    gl_stats: WeaponStats
    rl_stats: WeaponStats
    lg_stats: WeaponStats


@dataclasses.dataclass
class PlayerStatsMatch:
    match_info: MatchInfo
    match_user_id: str
    name: str
    login: str
    win: int
    player_stats: PlayerStats
